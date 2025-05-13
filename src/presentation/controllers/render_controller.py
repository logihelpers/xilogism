from presentation.states.render_state import RenderState
from presentation.states.viewing_mode_state import ViewingModeState, ViewingMode
from presentation.states.bom_state import BOMState
from presentation.states.dialogs_state import Dialogs, DialogState
from typing import List, Tuple, Dict, Any, Optional

from flet import *

from presentation.controllers.controller import Controller, Priority

from presentation.views.widgets.circuit_components.input_node import InputNode
from presentation.views.widgets.circuit_components.output_node import OutputNode
from presentation.views.widgets.circuit_components.wire import Wire
from presentation.views.widgets.circuit_components.gates.and_gate import ANDGate
from presentation.views.widgets.circuit_components.gates.or_gate import ORGate
from presentation.views.widgets.circuit_components.gates.xor_gate import XORGate
from presentation.views.widgets.circuit_components.gates.not_gate import NOTGate
from presentation.views.widgets.circuit_components.abstract_element import LogicElement
from presentation.views.widgets.circuit_components.gates.block import Block
from presentation.views.widgets.circuit_components.gates.comparator import Comparator

from presentation.views.widgets.circuit_components.ic.and_740x import AND740XIC
from presentation.views.widgets.circuit_components.ic.or_74x2 import OR74x2
from presentation.views.widgets.circuit_components.ic.xor_74x6 import XOR74x6
from presentation.views.widgets.circuit_components.ic.not_7404 import NOT7404

class RenderController(Controller):
    current_input: dict = None
    priority = Priority.NONE
    
    # Constants for layout with more emphasis on horizontal layout
    HORIZONTAL_SPACING = 180  # Increased space between hierarchy levels
    VERTICAL_SPACING = 60     # Reduced vertical spacing between nodes
    MARGIN_LEFT = 50          # Left margin
    INPUT_MARGIN_TOP = 50     # INPUT Top margin
    BLOCK_MARGIN_TOP = 130    # BLOCK Top margin
    OUTPUT_MARGIN_TOP = 100   # OUTPUT Top Margin
    
    # Constants for IC Layout
    IC_HORIZONTAL_SPACING = 180  # Wider spacing for ICs
    IC_VERTICAL_SPACING = 160    # More vertical space for ICs
    
    def __init__(self, page: Page):
        self.page = page
        self.render_state = RenderState()
        self.render_state.on_input_change = self.process_input
        self.vm_state = ViewingModeState()
        self.vm_state.on_change = lambda: self.process_input(self.current_input)
        self.bom_state = BOMState()
        self.bom_state.on_bom_request = self.request_bom
        self.dia_state = DialogState()

        self.node_map = {}  # Maps node names to rendered components
        self.node_positions = {}  # Track the position of each node
        self.gates_by_hierarchy = {}  # Group gates by hierarchy level
    
    def request_bom(self):
        if not self.bom_state.show_bom:
            return
        
        self.bom_state.counts = self.count_gates(self.current_input)
        self.dia_state.state = Dialogs.BOM
        self.bom_state.show_bom = False
    
    def count_gates(self, process_output):
        gate_counts = {}
        
        # Assuming the process_output is a dict with a single key like 'OWEN'
        for system_key in process_output:
            nodes = process_output[system_key]
            for node in nodes.values():
                if node.get('type') == 'BLOCK':
                    block_type = node.get('block_type')
                    if block_type:
                        gate_counts[block_type] = gate_counts.get(block_type, 0) + 1
        
        return gate_counts

    def process_input(self, input: dict):
        """Main entry point to process the input dictionary and create visual elements"""
        if not input:
            return
            
        key_name, input_dict = input.popitem()
        nodes = []

        self.current_input = {key_name: input_dict}

        # Reset tracking dictionaries
        self.node_map = {}
        self.node_positions = {}
        self.gates_by_hierarchy = {}
        
        # First pass: analyze the hierarchy structure
        max_hierarchy = self._analyze_hierarchy(input_dict)
        
        # Second pass: create nodes by hierarchy
        if self.vm_state.state == ViewingMode.LOGIC:
            self._create_all_nodes(nodes, input_dict, max_hierarchy, use_ic=False)
        elif self.vm_state.state == ViewingMode.CIRCUIT:  # IC mode
            self._create_all_nodes(nodes, input_dict, max_hierarchy, use_ic=True)
        
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
    
    def _create_all_nodes(self, nodes: List, input_dict: Dict[str, Any], max_hierarchy: int, use_ic: bool = False):
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
                    self._create_block_nodes(nodes, blocks, hierarchy, use_ic)
                # Wires are created later in the connection phase
                if outputs:
                    self._create_output_nodes(nodes, outputs, hierarchy)
    
    def _create_input_nodes(self, nodes: List, input_nodes: List[Tuple[str, Dict]]):
        """Create input node components - arranged horizontally (left to right)"""
        for i, (name, info) in enumerate(input_nodes):
            # Position input nodes horizontally with improved spacing
            x = self.MARGIN_LEFT + (i * 80)  # Closer horizontal spacing for inputs
            y = self.INPUT_MARGIN_TOP
            
            input_node = InputNode(x, y)
            nodes.append(input_node)
            
            # Store reference to the visual component
            self.node_map[name] = input_node
            self.node_positions[name] = (x, y)
    
    def _create_output_nodes(self, nodes: List, output_nodes: List[Tuple[str, Dict]], hierarchy: int):
        """Create output node components - arranged horizontally"""
        # Calculate the total horizontal distance based on max hierarchy
        rightmost_x = self.MARGIN_LEFT + ((hierarchy + 1) * (self.HORIZONTAL_SPACING * 0.6))
        
        for i, (name, info) in enumerate(output_nodes):
            # Place outputs at the rightmost hierarchy level, but distribute horizontally
            x = rightmost_x
            # Distribute outputs horizontally when there are multiple
            if len(output_nodes) > 1:
                y = self.OUTPUT_MARGIN_TOP + (i * self.VERTICAL_SPACING)
            else:
                y = self.OUTPUT_MARGIN_TOP + (self.VERTICAL_SPACING * 1.5)  # Center single output
            
            output_node = OutputNode(x, y)
            nodes.append(output_node)
            
            # Store reference to the visual component
            self.node_map[name] = output_node
            self.node_positions[name] = (x, y)
    
    def _create_block_nodes(self, nodes: List, blocks: List[Tuple[str, Dict]], hierarchy: int, use_ic: bool = False):
        """Create logic gate or IC components with appropriate layout"""
        # Calculate the number of blocks at this hierarchy level
        total_blocks = len(blocks)
        
        # Group blocks by common input patterns
        blocks_by_input = self._group_blocks_by_common_inputs(blocks)
        
        # Adjust spacing based on rendering mode
        horiz_spacing = self.IC_HORIZONTAL_SPACING if use_ic else self.HORIZONTAL_SPACING
        vert_spacing = self.IC_VERTICAL_SPACING if use_ic else self.VERTICAL_SPACING
        
        # Process each input group with appropriate layout
        x_base = self.MARGIN_LEFT + (hierarchy * horiz_spacing)
        y_offset = 0
        
        for input_group, group_blocks in blocks_by_input.items():
            # Calculate vertical range for this group
            group_height = len(group_blocks) * vert_spacing
            
            # Position gates in a more horizontal arrangement
            for i, (name, info) in enumerate(group_blocks):
                # Add slight horizontal offset within the same hierarchy level
                x_offset = (i % 2) * 40 if not use_ic else 0  # No zigzag for ICs
                x = x_base + x_offset
                y = self.BLOCK_MARGIN_TOP + y_offset + (i * vert_spacing)
                
                # Create the appropriate component based on mode
                if use_ic:
                    component = self._create_ic_by_type(name, info, x, y)
                else:
                    component = self._create_gate_by_type(name, info, x, y)
                    
                if component:
                    nodes.append(component)
                    self.node_map[name] = component
                    self.node_positions[name] = (x, y)
            
            # Add spacing between groups
            spacing_factor = 0.5 if use_ic else 0.3
            y_offset += group_height + (vert_spacing * spacing_factor)
    
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
        """Create the appropriate logic gate based on the block type"""
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
            return Block(x, y, block_type=str(block_type))  # Placeholder
        elif block_type in ["COMPARATOR"]:
            # For comparison operations
            return Comparator(x, y, block_type=str(block_type))  # Placeholder
        
        # Default to AND gate for unknown types
        return Block(x, y, input_count=input_count)
    
    def _create_ic_by_type(self, name: str, info: Dict[str, Any], x: int, y: int) -> Optional[LogicElement]:
        """Create the appropriate IC based on the block type"""
        block_type = info.get("block_type", "")
        
        # Match block type to create appropriate IC
        if block_type in ["AND", "NAND"]:
            return AND740XIC(x, y, nand=(block_type == "NAND"))
        elif block_type in ["OR", "NOR"]:
            return OR74x2(x, y, nor=(block_type == "NOR"))
        elif block_type == "NOT":
            return NOT7404(x, y)
        elif block_type in ["XOR", "XNOR"]:
            return XOR74x6(x, y, xnor=(block_type == "XNOR"))
        elif block_type in ["ADD", "ADDER", "SUBTRACTOR", "MULTIPLIER", "DIVIDER", "MODULO"]:
            # Use generic ICs for arithmetic operations (could be customized further)
            return AND740XIC(x, y)  # Placeholder
        elif block_type in ["COMPARATOR"]:
            # For comparison operations
            return AND740XIC(x, y)  # Placeholder
        
        # Default to AND IC for unknown types
        return AND740XIC(x, y)
    
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
        
        # Process output connections
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