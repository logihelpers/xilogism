import re
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set, Optional, Union, Deque
from collections import deque


@dataclass
class LogicGate:
    """Represents a logic gate in the circuit"""
    gate_id: str
    gate_type: str  # AND, OR, NOT, COMP, etc.
    inputs: List[str]  # IDs of input gates or variables
    label: str = ""  # Optional display label
    
    def __str__(self):
        return f"{self.gate_id}({self.gate_type}: {','.join(self.inputs)})"


class LogicCircuit:
    """Represents a complete logic circuit with multiple gates"""
    
    def __init__(self):
        self.gates: Dict[str, LogicGate] = {}
        self.inputs: Set[str] = set()
        self.outputs: Dict[str, str] = {}  # output_name -> gate_id
        self.gate_counter = 0
    
    def add_gate(self, gate_type: str, inputs: List[str], label: str = "") -> str:
        """Add a gate to the circuit and return its ID"""
        gate_id = f"g{self.gate_counter}"
        self.gate_counter += 1
        
        self.gates[gate_id] = LogicGate(gate_id, gate_type, inputs, label)
        return gate_id
    
    def add_input(self, input_name: str) -> None:
        """Add an input to the circuit"""
        self.inputs.add(input_name)
    
    def set_output(self, output_name: str, gate_id: str) -> None:
        """Set a gate as an output of the circuit"""
        self.outputs[output_name] = gate_id
    
    def __str__(self):
        result = ["Logic Circuit:"]
        result.append(f"Inputs: {', '.join(sorted(self.inputs))}")
        result.append(f"Outputs: {', '.join(f'{name}={gate_id}' for name, gate_id in self.outputs.items())}")
        result.append("Gates:")
        for gate_id, gate in sorted(self.gates.items()):
            result.append(f"  {gate}")
        return "\n".join(result)
    
    def to_svg(self, width=800, height=600) -> str:
        """Generate an SVG representation of the circuit"""
        # We'll do a simple layout with input variables on the left,
        # gates in the middle arranged in levels, and outputs on the right
        
        # Step 1: Determine the logic levels (gate dependencies)
        gate_levels = self._compute_gate_levels()
        max_level = max(gate_levels.values()) if gate_levels else 0
        
        # Step 2: Position gates based on their levels
        positions = self._compute_positions(gate_levels, max_level)
        
        # Step 3: Draw the SVG
        return self._generate_svg(positions, width, height)
    
    def _compute_gate_levels(self) -> Dict[str, int]:
        """Compute the level of each gate in the circuit using iterative approach"""
        levels: Dict[str, int] = {}
        
        # Initial pass: Assign level 0 to all inputs and constants
        for input_name in self.inputs:
            levels[input_name] = 0
        
        # Iteratively compute levels until all gates have levels
        # This avoids recursion and stack overflow
        changed = True
        while changed:
            changed = False
            
            for gate_id, gate in self.gates.items():
                # Skip gates that already have a level
                if gate_id in levels:
                    continue
                
                # Check if all inputs have levels
                all_inputs_have_levels = True
                max_input_level = 0
                
                for input_id in gate.inputs:
                    if input_id not in levels:
                        # This input doesn't have a level yet, can't process this gate
                        all_inputs_have_levels = False
                        break
                    max_input_level = max(max_input_level, levels[input_id])
                
                if all_inputs_have_levels:
                    # All inputs have levels, assign level to this gate
                    levels[gate_id] = max_input_level + 1
                    changed = True
        
        return levels
    
    def _compute_positions(self, gate_levels: Dict[str, int], max_level: int) -> Dict[str, Tuple[float, float]]:
        """Compute (x, y) positions for all gates and inputs"""
        positions: Dict[str, Tuple[float, float]] = {}
        
        # Group gates by level
        gates_by_level: Dict[int, List[str]] = {}
        for gate_id, level in gate_levels.items():
            if level not in gates_by_level:
                gates_by_level[level] = []
            gates_by_level[level].append(gate_id)
        
        # Add input variables at level 0
        input_vars = list(self.inputs)
        if 0 not in gates_by_level:
            gates_by_level[0] = []
        gates_by_level[0] = input_vars + gates_by_level[0]
        
        # Position gates
        x_spacing = 150
        y_spacing = 80
        x_margin = 50
        y_margin = 50
        
        for level, gate_ids in sorted(gates_by_level.items()):
            x = x_margin + level * x_spacing
            
            # Space gates evenly within each level
            for i, gate_id in enumerate(gate_ids):
                y = y_margin + i * y_spacing
                positions[gate_id] = (x, y)
        
        return positions
    
    def _generate_svg(self, positions: Dict[str, Tuple[float, float]], width: int, height: int) -> str:
        """Generate SVG for the circuit based on computed positions"""
        svg_elements = []
        
        # SVG header
        svg_elements.append(f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
        svg_elements.append('<style>')
        svg_elements.append('.gate { fill: white; stroke: black; stroke-width: 2; }')
        svg_elements.append('.wire { stroke: black; stroke-width: 2; }')
        svg_elements.append('.label { font-family: Arial; font-size: 12px; text-anchor: middle; }')
        svg_elements.append('.input-label { font-family: Arial; font-size: 14px; }')
        svg_elements.append('.output-label { font-family: Arial; font-size: 14px; }')
        svg_elements.append('</style>')
        
        # Draw wires first (so they appear behind gates)
        for gate_id, gate in self.gates.items():
            if gate_id in positions:
                gate_x, gate_y = positions[gate_id]
                
                # Determine input positions for the gate
                for input_id in gate.inputs:
                    if input_id in positions:
                        input_x, input_y = positions[input_id]
                        
                        # Simple wire routing
                        # For gates with multiple inputs, we need to adjust endpoints
                        if gate.gate_type in ["AND", "OR", "XOR"]:
                            # Calculate a suitable entry point on the gate based on input position
                            inputs_count = len(gate.inputs)
                            input_index = gate.inputs.index(input_id)
                            
                            gate_width = 60
                            gate_height = 40
                            
                            # Distribute input connections evenly along the left side of the gate
                            entry_y_offset = (input_index + 1) * gate_height / (inputs_count + 1) - gate_height / 2
                            gate_entry_x = gate_x - gate_width / 2
                            gate_entry_y = gate_y + entry_y_offset
                            
                            svg_elements.append(f'<path d="M {input_x + 30} {input_y} L {gate_entry_x} {gate_entry_y}" class="wire" />')
                        elif gate.gate_type == "NOT":
                            svg_elements.append(f'<path d="M {input_x + 30} {input_y} L {gate_x - 20} {gate_y}" class="wire" />')
                        else:
                            # Default wire
                            svg_elements.append(f'<path d="M {input_x + 30} {input_y} L {gate_x - 30} {gate_y}" class="wire" />')
        
        # Draw output wires
        for output_name, gate_id in self.outputs.items():
            if gate_id in positions:
                gate_x, gate_y = positions[gate_id]
                
                # Draw wire to the right edge
                output_x = width - 50
                svg_elements.append(f'<path d="M {gate_x + 30} {gate_y} L {output_x} {gate_y}" class="wire" />')
                
                # Output label
                svg_elements.append(f'<text x="{output_x + 20}" y="{gate_y + 5}" class="output-label">{output_name}</text>')
        
        # Draw gates
        for gate_id, gate in self.gates.items():
            if gate_id in positions:
                gate_x, gate_y = positions[gate_id]
                
                # Draw gate based on type
                if gate.gate_type == "AND":
                    self._draw_and_gate(svg_elements, gate_x, gate_y, gate.label)
                elif gate.gate_type == "OR":
                    self._draw_or_gate(svg_elements, gate_x, gate_y, gate.label)
                elif gate.gate_type == "NOT":
                    self._draw_not_gate(svg_elements, gate_x, gate_y, gate.label)
                elif gate.gate_type == "COMP":
                    self._draw_comparator(svg_elements, gate_x, gate_y, gate.label)
                elif gate.gate_type == "XOR":
                    self._draw_xor_gate(svg_elements, gate_x, gate_y, gate.label)
                else:
                    # Default gate representation
                    self._draw_generic_gate(svg_elements, gate_x, gate_y, gate.gate_type, gate.label)
        
        # Draw input variables
        for input_var in self.inputs:
            if input_var in positions:
                input_x, input_y = positions[input_var]
                
                # Draw input symbol (just a label for simplicity)
                svg_elements.append(f'<text x="{input_x}" y="{input_y + 5}" class="input-label">{input_var}</text>')
        
        # SVG footer
        svg_elements.append('</svg>')
        
        return '\n'.join(svg_elements)
    
    def _draw_and_gate(self, svg_elements, x, y, label=""):
        """Draw an AND gate"""
        svg_elements.append(f'<path d="M {x-30} {y-20} L {x-30} {y+20} L {x} {y+20} A 20 20 0 0 0 {x} {y-20} L {x-30} {y-20}" class="gate" />')
        svg_elements.append(f'<text x="{x-10}" y="{y+5}" class="label">AND</text>')
        if label:
            svg_elements.append(f'<text x="{x}" y="{y-25}" class="label">{label}</text>')
    
    def _draw_or_gate(self, svg_elements, x, y, label=""):
        """Draw an OR gate"""
        svg_elements.append(f'<path d="M {x-30} {y-20} Q {x-10} {y-20} {x} {y} Q {x-10} {y+20} {x-30} {y+20} Q {x-40} {y} {x-30} {y-20}" class="gate" />')
        svg_elements.append(f'<text x="{x-15}" y="{y+5}" class="label">OR</text>')
        if label:
            svg_elements.append(f'<text x="{x}" y="{y-25}" class="label">{label}</text>')
    
    def _draw_not_gate(self, svg_elements, x, y, label=""):
        """Draw a NOT gate (inverter)"""
        svg_elements.append(f'<path d="M {x-20} {y-15} L {x-20} {y+15} L {x+10} {y} Z" class="gate" />')
        svg_elements.append(f'<circle cx="{x+15}" cy="{y}" r="5" class="gate" />')
        if label:
            svg_elements.append(f'<text x="{x}" y="{y-20}" class="label">{label}</text>')
    
    def _draw_xor_gate(self, svg_elements, x, y, label=""):
        """Draw an XOR gate"""
        svg_elements.append(f'<path d="M {x-35} {y-20} Q {x-15} {y-20} {x} {y} Q {x-15} {y+20} {x-35} {y+20} Q {x-45} {y} {x-35} {y-20}" class="gate" />')
        svg_elements.append(f'<path d="M {x-40} {y-20} Q {x-20} {y-20} {x-5} {y} Q {x-20} {y+20} {x-40} {y+20}" class="wire" fill="none" />')
        svg_elements.append(f'<text x="{x-20}" y="{y+5}" class="label">XOR</text>')
        if label:
            svg_elements.append(f'<text x="{x}" y="{y-25}" class="label">{label}</text>')
    
    def _draw_comparator(self, svg_elements, x, y, label=""):
        """Draw a comparator"""
        svg_elements.append(f'<rect x="{x-30}" y="{y-20}" width="60" height="40" rx="5" ry="5" class="gate" />')
        svg_elements.append(f'<text x="{x}" y="{y+5}" class="label">COMP</text>')
        if label:
            svg_elements.append(f'<text x="{x}" y="{y-5}" class="label">{label}</text>')
    
    def _draw_generic_gate(self, svg_elements, x, y, gate_type, label=""):
        """Draw a generic gate"""
        svg_elements.append(f'<rect x="{x-30}" y="{y-20}" width="60" height="40" rx="5" ry="5" class="gate" />')
        svg_elements.append(f'<text x="{x}" y="{y+5}" class="label">{gate_type}</text>')
        if label:
            svg_elements.append(f'<text x="{x}" y="{y-5}" class="label">{label}</text>')


class BooleanToCircuitConverter:
    """Converts Boolean algebra expressions to logic circuits"""
    
    def __init__(self):
        self.circuit = LogicCircuit()
        self.expr_cache = {}  # Cache for subexpressions to prevent duplicates
    
    def convert(self, expr: str) -> LogicCircuit:
        """Convert boolean expression to logic circuit"""
        self.circuit = LogicCircuit()
        self.expr_cache = {}
        
        # Parse the overall expression (might contain multiple cases)
        parts = expr.split(' | ')
        
        output_gates = []
        for part in parts:
            # Parse each part (condition → output)
            if '→' in part:
                condition, output = part.split('→')
                condition = condition.strip()
                output_match = re.match(r'([a-zA-Z0-9_]+)=(.+)', output.strip())
                
                if output_match:
                    output_var = output_match.group(1)
                    output_val = output_match.group(2)
                    
                    # Parse the condition to build a subcircuit
                    condition_gate = self._parse_expression(condition)
                    
                    # For each distinct output value, create a gate
                    if output_val not in self.expr_cache:
                        # This is a constant output value
                        output_gates.append((condition_gate, output_var, output_val))
                    else:
                        # This is a reference to another gate
                        output_gates.append((condition_gate, output_var, self.expr_cache[output_val]))
        
        # Now create the final output logic
        if output_gates:
            # Group by output variable
            outputs_by_var = {}
            for condition_gate, output_var, output_val in output_gates:
                if output_var not in outputs_by_var:
                    outputs_by_var[output_var] = []
                outputs_by_var[output_var].append((condition_gate, output_val))
            
            # Create logic for each output variable
            for output_var, gates_and_vals in outputs_by_var.items():
                # For simple cases, we can connect the condition directly to the output
                if len(gates_and_vals) == 1:
                    self.circuit.set_output(output_var, gates_and_vals[0][0])
                else:
                    # For multiple conditions, we need a multiplexer-like structure
                    # For simplicity, use an OR gate to combine conditions
                    condition_gates = [gate for gate, _ in gates_and_vals]
                    output_gate = self.circuit.add_gate("OR", condition_gates, f"{output_var}")
                    self.circuit.set_output(output_var, output_gate)
        
        return self.circuit
    
    def _parse_expression(self, expr: str) -> str:
        """Parse a boolean expression and add the corresponding gates to the circuit"""
        # Use iterative approach instead of recursion to avoid stack overflow
        stack = [expr]
        result_stack = []
        
        while stack:
            current_expr = stack.pop()
            
            # If we've already evaluated this expression, use the cached result
            if current_expr in self.expr_cache:
                result_stack.append(self.expr_cache[current_expr])
                continue
            
            # Strip whitespace and handle basic parentheses
            current_expr = current_expr.strip()
            if current_expr.startswith('(') and current_expr.endswith(')'):
                if self._find_matching_paren(current_expr, 0) == len(current_expr) - 1:
                    current_expr = current_expr[1:-1].strip()
            
            # Check for operators
            if ' · ' in current_expr:  # AND operation
                subexprs = self._split_by_operator(current_expr, ' · ')
                # Process each subexpression
                gate_inputs = []
                
                for subexpr in subexprs:
                    if subexpr in self.expr_cache:
                        gate_inputs.append(self.expr_cache[subexpr])
                    else:
                        # Push back for more processing
                        stack.append(current_expr)
                        for s in reversed(subexprs):  # Push in reverse order
                            stack.append(s)
                        break
                else:
                    # All subexpressions processed
                    gate_id = self.circuit.add_gate("AND", gate_inputs)
                    self.expr_cache[current_expr] = gate_id
                    result_stack.append(gate_id)
                
            elif ' + ' in current_expr:  # OR operation
                subexprs = self._split_by_operator(current_expr, ' + ')
                # Process each subexpression
                gate_inputs = []
                
                for subexpr in subexprs:
                    if subexpr in self.expr_cache:
                        gate_inputs.append(self.expr_cache[subexpr])
                    else:
                        # Push back for more processing
                        stack.append(current_expr)
                        for s in reversed(subexprs):  # Push in reverse order
                            stack.append(s)
                        break
                else:
                    # All subexpressions processed
                    gate_id = self.circuit.add_gate("OR", gate_inputs)
                    self.expr_cache[current_expr] = gate_id
                    result_stack.append(gate_id)
                
            elif current_expr.startswith('¬'):  # NOT operation
                # Extract the expression to negate
                subexpr = current_expr[1:].strip()
                if subexpr.startswith('(') and subexpr.endswith(')'):
                    subexpr = subexpr[1:-1].strip()
                
                if subexpr in self.expr_cache:
                    gate_id = self.circuit.add_gate("NOT", [self.expr_cache[subexpr]])
                    self.expr_cache[current_expr] = gate_id
                    result_stack.append(gate_id)
                else:
                    # Push back for more processing
                    stack.append(current_expr)
                    stack.append(subexpr)
                
            else:
                # This is a variable or comparison (leaf node)
                self.circuit.add_input(current_expr)
                self.expr_cache[current_expr] = current_expr
                result_stack.append(current_expr)
        
        # Return the final result
        if result_stack:
            return result_stack[-1]
        else:
            # Default fallback if something went wrong
            return "error"
    
    def _find_matching_paren(self, expr: str, start_pos: int) -> int:
        """Find the matching closing parenthesis for the one at start_pos"""
        if expr[start_pos] != '(':
            return -1
        
        count = 1
        for i in range(start_pos + 1, len(expr)):
            if expr[i] == '(':
                count += 1
            elif expr[i] == ')':
                count -= 1
                if count == 0:
                    return i
        
        return -1
    
    def _split_by_operator(self, expr: str, op: str) -> List[str]:
        """Split an expression by an operator, respecting parentheses"""
        result = []
        start = 0
        i = 0
        
        while i < len(expr):
            if expr[i] == '(':
                # Skip to matching closing parenthesis
                closing_pos = self._find_matching_paren(expr, i)
                if closing_pos == -1:
                    # No matching parenthesis found
                    break
                i = closing_pos
            
            elif i <= len(expr) - len(op) and expr[i:i+len(op)] == op:
                # Found the operator
                result.append(expr[start:i].strip())
                start = i + len(op)
                i += len(op) - 1  # -1 because the loop will increment i
            
            i += 1
        
        # Add the last part
        if start < len(expr):
            result.append(expr[start:].strip())
        
        return result


# def main():
#     # Example boolean expression
#     bool_expr = "(ok<10.0 · ok>0.0) → uk=10.0 | (ok<0.0 · ok>-10.0) → uk=-10.0 | ¬((ok<10.0 · ok>0.0)) · ¬((ok<0.0 · ok>-10.0)) → uk=10.0"
    
#     # Convert to logic circuit
#     converter = BooleanToCircuitConverter()
#     circuit = converter.convert(bool_expr)
    
#     print("Logic Circuit Structure:")
#     print(circuit)
    
#     # Generate SVG representation
#     svg = circuit.to_svg(800, 500)
    
#     print("\nSVG Representation:")
#     print(svg[:200] + "... (truncated)")
    
#     # Save to file
#     with open("logic_circuit_fixed.svg", "w") as f:
#         f.write(svg)
#     print("\nSaved SVG to logic_circuit_fixed.svg")


# if __name__ == "__main__":
#     main()