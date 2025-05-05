from presentation.states.render_state import RenderState
from models.xilofile_model import XiloFile
from typing import List, Tuple, Dict, Any, Optional
import math

from flet import *

from presentation.controllers.controller import Controller, Priority

from presentation.views.widgets.logic_circuit.input_node import InputNode
from presentation.views.widgets.logic_circuit.output_node import OutputNode
from presentation.views.widgets.logic_circuit.wire import Wire
from presentation.views.widgets.logic_circuit.gates.and_gate import ANDGate
from presentation.views.widgets.logic_circuit.gates.or_gate import ORGate
from presentation.views.widgets.logic_circuit.gates.xor_gate import XORGate
from presentation.views.widgets.logic_circuit.gates.not_gate import NOTGate
from presentation.views.widgets.logic_circuit.abstract_element import LogicElement

class RenderController(Controller):
    priority = Priority.NONE
    
    # Constants for layout
    HORIZONTAL_SPACING = 150  # Space between hierarchy levels
    VERTICAL_SPACING = 80     # Base vertical spacing between nodes
    MARGIN_LEFT = 50         # Left margin
    MARGIN_TOP = 50          # Top margin
    
    def __init__(self, page: Page):
        self.page = page
        self.render_state = RenderState()
        self.render_state.on_input_change = self.process_input
        self.node_map = {}  # Maps node names to rendered components
        self.node_positions = {}  # Track the position of each node
        self.gates_by_hierarchy = {}  # Group gates by hierarchy level

    def process_input(self, input: dict):
        """Main entry point to process the input dictionary and create visual elements"""
        print("_____START_____")
        key_name, input_dict = input.popitem()
        nodes = []

        print(input_dict)
        
        # Reset tracking dictionaries
        self.node_map = {}
        self.node_positions = {}
        self.gates_by_hierarchy = {}
        
        # First pass: analyze the hierarchy structure
        max_hierarchy = self._analyze_hierarchy(input_dict)
        
        # Second pass: create nodes by hierarchy
        self._create_all_nodes(nodes, input_dict, max_hierarchy)
        
        # Third pass: create connections
        wires = self._create_connections(input_dict)
        
        # Combine all elements
        all_elements = nodes + wires
        self.render_state.output[key_name] = all_elements
    
    def _analyze_hierarchy(self, input_dict: Dict[str, Any]) -> int:
        """Analyze hierarchy structure and group nodes by hierarchy level"""
        max_hierarchy = 0
        for node_name, node_info in input_dict.items():
            hierarchy = node_info.get("hierarchy", 0)
            max_hierarchy = max(max_hierarchy, hierarchy)
            
            if hierarchy not in self.gates_by_hierarchy:
                self.gates_by_hierarchy[hierarchy] = []
            self.gates_by_hierarchy[hierarchy].append((node_name, node_info))
        
        return max_hierarchy
    
    def _create_all_nodes(self, nodes: List, input_dict: Dict[str, Any], max_hierarchy: int):
        """Create all node visual elements ordered by hierarchy"""
        # Create nodes by hierarchy level, from lowest to highest
        for hierarchy in range(max_hierarchy + 1):
            if hierarchy in self.gates_by_hierarchy:
                hierarchy_nodes = self.gates_by_hierarchy[hierarchy]
                
                # Sort by type for consistent ordering: inputs first, then blocks, then wires
                inputs = [(n, i) for n, i in hierarchy_nodes if i["type"] == "INPUT_NODE"]
                blocks = [(n, i) for n, i in hierarchy_nodes if i["type"] == "BLOCK"]
                wires = [(n, i) for n, i in hierarchy_nodes if i["type"] == "WIRE"]
                outputs = [(n, i) for n, i in hierarchy_nodes if i["type"] == "OUTPUT_NODE"]
                
                # Process each type
                if inputs:
                    self._create_input_nodes(nodes, inputs)
                if blocks:
                    self._create_block_nodes(nodes, blocks, hierarchy)
                # Wires are created later in the connection phase
                if outputs:
                    self._create_output_nodes(nodes, outputs, hierarchy)
    
    def _create_input_nodes(self, nodes: List, input_nodes: List[Tuple[str, Dict]]):
        """Create input node components - arranged horizontally (left to right)"""
        for i, (name, info) in enumerate(input_nodes):
            # Position input nodes horizontally instead of vertically
            x = self.MARGIN_LEFT + (i * self.HORIZONTAL_SPACING * 0.6)  # Slightly closer spacing for inputs
            y = self.MARGIN_TOP
            
            input_node = InputNode(x, y)
            nodes.append(input_node)
            
            # Store reference to the visual component
            self.node_map[name] = input_node
            self.node_positions[name] = (x, y)
    
    def _create_output_nodes(self, nodes: List, output_nodes: List[Tuple[str, Dict]], hierarchy: int):
        """Create output node components"""
        for i, (name, info) in enumerate(output_nodes):
            # Place outputs at the rightmost hierarchy level
            x = self.MARGIN_LEFT + ((hierarchy + 1) * self.HORIZONTAL_SPACING)
            y = self.MARGIN_TOP + (i * self.VERTICAL_SPACING)
            
            output_node = OutputNode(x, y)
            nodes.append(output_node)
            
            # Store reference to the visual component
            self.node_map[name] = output_node
            self.node_positions[name] = (x, y)
    
    def _create_block_nodes(self, nodes: List, blocks: List[Tuple[str, Dict]], hierarchy: int):
        """Create logic gate components for blocks with improved positioning"""
        # Calculate vertical distribution
        total_blocks = len(blocks)
        
        # Group blocks by their inputs to improve layout
        blocks_by_input = self._group_blocks_by_common_inputs(blocks)
        
        # Process each input group separately
        y_offset = 0
        for input_group, group_blocks in blocks_by_input.items():
            for i, (name, info) in enumerate(group_blocks):
                x = self.MARGIN_LEFT + (hierarchy * self.HORIZONTAL_SPACING)
                # Distribute nodes vertically with proper spacing between groups
                y = self.MARGIN_TOP + y_offset + (i * self.VERTICAL_SPACING)
                
                # Create the appropriate gate based on block_type
                gate = self._create_gate_by_type(name, info, x, y)
                if gate:
                    nodes.append(gate)
                    self.node_map[name] = gate
                    self.node_positions[name] = (x, y)
            
            # Add extra spacing between groups
            y_offset += len(group_blocks) * self.VERTICAL_SPACING + (self.VERTICAL_SPACING * 0.5)
    
    def _group_blocks_by_common_inputs(self, blocks: List[Tuple[str, Dict]]) -> Dict[str, List[Tuple[str, Dict]]]:
        """Group blocks by their common input sources to improve layout"""
        groups = {}
        ungrouped = []
        
        # First try to group by primary input
        for name, info in blocks:
            inputs = info.get("inputs", [])
            if inputs:
                primary_input = inputs[0]
                if primary_input not in groups:
                    groups[primary_input] = []
                groups[primary_input].append((name, info))
            else:
                ungrouped.append((name, info))
        
        # Add ungrouped elements to a default group
        if ungrouped:
            groups["_ungrouped"] = ungrouped
            
        return groups
    
    def _create_gate_by_type(self, name: str, info: Dict[str, Any], x: int, y: int) -> Optional[LogicElement]:
        """Create the appropriate gate based on the block type"""
        block_type = info.get("block_type", "")
        
        # Count inputs for the gate
        input_count = len(info.get("inputs", []))
        if input_count < 2:
            input_count = 2  # Minimum input count
        
        # Match block type to create appropriate gate
        if block_type in ["AND", "NAND"]:
            return ANDGate(x, y, input_count=input_count, nand=(block_type == "NAND"))
        elif block_type in ["OR", "NOR"]:
            return ORGate(x, y, input_count=input_count, nor=(block_type == "NOR"))
        elif block_type == "NOT":
            return NOTGate(x, y)
        elif block_type in ["XOR", "XNOR"]:
            return XORGate(x, y, input_count=input_count, xnor=(block_type == "XNOR"))
        elif block_type == "ADD":  # Changed from ADDER to ADD to match "+" in assign statement
            # For addition operation (OR gate)
            return ORGate(x, y, input_count=input_count)
        elif block_type in ["ADDER", "SUBTRACTOR", "MULTIPLIER", "DIVIDER", "MODULO"]:
            # Arithmetic operations - could use custom block representation
            return ANDGate(x, y, input_count=input_count)  # Placeholder
        elif block_type in ["COMPARATOR"]:
            # For comparison operations
            return ANDGate(x, y, input_count=2)  # Placeholder
        
        # Default to AND gate for unknown types
        return ANDGate(x, y, input_count=input_count)
    
    def _create_connections(self, input_dict: Dict[str, Any]) -> List[Wire]:
        """Create wire connections between components"""
        wires = []
        processed_connections = set()  # Track processed connections to avoid duplicates
        
        # Process direct wire connections
        for name, info in input_dict.items():
            if info["type"] == "WIRE":
                # Connect 'from' to 'to'
                from_node = info.get("from")
                to_node = info.get("to")
                
                connection_key = f"{from_node}->{to_node}"
                if connection_key not in processed_connections:
                    if from_node in self.node_map and to_node in self.node_map:
                        wire = Wire(self.node_map[from_node], self.node_map[to_node])
                        wires.append(wire)
                        processed_connections.add(connection_key)
        
        # Process block input connections
        for name, info in input_dict.items():
            if info["type"] == "BLOCK":
                # Connect inputs to this block
                inputs = info.get("inputs", [])
                
                if name in self.node_map:
                    target = self.node_map[name]
                    
                    for i, input_name in enumerate(inputs):
                        connection_key = f"{input_name}->{name}"
                        if connection_key not in processed_connections:
                            if input_name in self.node_map:
                                # Connect to the appropriate input position
                                try:
                                    wire = Wire(self.node_map[input_name], target, min(i, len(target.input_coord)-1))
                                    wires.append(wire)
                                    processed_connections.add(connection_key)
                                except Exception as e:
                                    # Fallback if there are issues with multiple input positions
                                    wire = Wire(self.node_map[input_name], target, 0)
                                    wires.append(wire)
                                    processed_connections.add(connection_key)
        
        # NEW: Process output connections
        for name, info in input_dict.items():
            if info["type"] == "OUTPUT_NODE":
                # Find blocks that have this output in their outputs list
                input_sources = info.get("inputs", [])
                
                if name in self.node_map:
                    target = self.node_map[name]
                    
                    # Connect each input source to this output
                    for input_source in input_sources:
                        connection_key = f"{input_source}->{name}"
                        if connection_key not in processed_connections:
                            if input_source in self.node_map:
                                wire = Wire(self.node_map[input_source], target)
                                wires.append(wire)
                                processed_connections.add(connection_key)
        
        return wires