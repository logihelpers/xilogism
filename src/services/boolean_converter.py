import re

class BooleanConverter:
    def __init__(self):
        self.nodes = {}
        self.counter = {
            "constant": 0,
            "multiplier": 0,
            "comparator": 0,
            "adder": 0,
            "subtractor": 0,
            "logic": 0,
            "wire": 0,
            "xor": 0,
            "and": 0,
            "or": 0,
            "not": 0,
            "nand": 0,
            "nor": 0,
            "xnor": 0
        }
        self.max_hierarchy = 0
        self.variables = {}  # Track variable assignments
        self.output_connections = {}  # Track which nodes feed into outputs

    def _new_name(self, prefix):
        self.counter[prefix] += 1
        return f"{prefix}_{self.counter[prefix]}"

    def simplify_condition(self, condition: str):
        # Basic simplification: identify simple comparators and logic ops
        if any(op in condition for op in ["<", ">", "==", "!=", "<=", ">=", "&&", "||"]):
            return condition.strip()
        else:
            return condition.replace(" ", "").strip()
    
    def _parse_condition(self, condition):
        """Parse a condition into its components for better representation"""
        # Handle simple variable conditions (treat as comparison with True)
        if " " not in condition and not any(op in condition for op in ["<", ">", "==", "!=", "<=", ">=", "&&", "||", "&", "|", "^"]):
            return {
                "type": "SIMPLE",
                "variable": condition,
                "op": "==",
                "value": "True"
            }
        
        # Handle complex conditions with logical operators
        if "&&" in condition or "||" in condition:
            if "&&" in condition:
                parts = condition.split("&&")
                return {
                    "type": "LOGICAL",
                    "op": "AND",
                    "conditions": [self._parse_condition(part.strip()) for part in parts]
                }
            elif "||" in condition:
                parts = condition.split("||")
                return {
                    "type": "LOGICAL",
                    "op": "OR",
                    "conditions": [self._parse_condition(part.strip()) for part in parts]
                }
        
        # Handle comparison operators
        for op in ["==", "!=", "<=", ">=", "<", ">"]:
            if op in condition:
                left, right = condition.split(op, 1)
                return {
                    "type": "COMPARISON",
                    "left": left.strip(),
                    "op": op,
                    "right": right.strip()
                }
        
        # Handle bitwise operations
        for op, name in [("&", "AND"), ("|", "OR"), ("^", "XOR")]:
            if op in condition and f"{op}{op}" not in condition:  # Avoid misinterpreting && as &
                parts = condition.split(op)
                return {
                    "type": "BITWISE",
                    "op": name,
                    "operands": [part.strip() for part in parts]
                }
        
        # Default fallback
        return {
            "type": "RAW",
            "expression": condition
        }

    def add_constant(self, value):
        name = f"constant_{value}" if isinstance(value, int) else self._new_name("constant")
        if name not in self.nodes:
            self.nodes[name] = {
                "type": "CONSTANT",
                "value": value,
                "hierarchy": 0
            }
        return name

    def process_expr(self, expr, from_var):
        expr = expr.strip()
        hierarchy_level = 1
        
        # Handle parentheses expressions first
        if expr.startswith("(") and expr.endswith(")"):
            # Process the inner expression directly
            inner_expr = expr[1:-1].strip()
            return self.process_expr(inner_expr, from_var)
        
        # Check for logic operations with keywords
        logic_ops = {
            "and(": "AND",
            "or(": "OR", 
            "xor(": "XOR",
            "not(": "NOT",
            "nand(": "NAND",
            "nor(": "NOR",
            "xnor(": "XNOR"
        }
        
        for op_keyword, gate_type in logic_ops.items():
            if op_keyword in expr.lower():
                # Extract arguments inside parentheses
                start_idx = expr.lower().find(op_keyword) + len(op_keyword)
                # Find matching closing parenthesis
                open_count = 1
                end_idx = start_idx
                while open_count > 0 and end_idx < len(expr):
                    if expr[end_idx] == '(':
                        open_count += 1
                    elif expr[end_idx] == ')':
                        open_count -= 1
                    end_idx += 1
                
                if open_count == 0:
                    args_str = expr[start_idx:end_idx-1]
                    args = [arg.strip() for arg in args_str.split(',')]
                    processed_args = []
                    
                    for arg in args:
                        processed_arg = self.process_expr(arg, from_var)
                        processed_args.append(processed_arg)
                    
                    gate_name = self._new_name(gate_type.lower())
                    hierarchy_level = 2  # Logic gates get higher hierarchy
                    self.nodes[gate_name] = {
                        "type": "BLOCK",
                        "block_type": gate_type,
                        "inputs": processed_args,
                        "output": gate_name,
                        "hierarchy": hierarchy_level
                    }
                    self.max_hierarchy = max(self.max_hierarchy, hierarchy_level)
                    
                    # Track this output for later connection to destination
                    if from_var in self.nodes and self.nodes[from_var]["type"] == "OUTPUT_NODE":
                        if from_var not in self.output_connections:
                            self.output_connections[from_var] = []
                        self.output_connections[from_var].append(gate_name)
                    
                    return gate_name
        
        # Subtraction handling (using XOR and NOT gates)
        if "-" in expr and not expr.startswith("-"):  # Ensure it's subtraction, not negative number
            terms = [t.strip() for t in expr.split("-", 1)]  # Split only on first occurrence
            subtractor_name = self._new_name("subtractor")
            
            # Process minuend and subtrahend
            minuend = self.process_expr(terms[0], from_var)
            subtrahend = self.process_expr(terms[1], from_var)
            
            # For binary subtraction A-B:
            # First create the NOT gate (hierarchy level 1)
            not_name = self._new_name("not")
            not_hierarchy = 1  # Set NOT gate to lowest hierarchy level
            self.nodes[not_name] = {
                "type": "BLOCK",
                "block_type": "NOT",
                "inputs": [minuend],
                "output": not_name,
                "hierarchy": not_hierarchy
            }
            
            # Then create the AND gate for borrow (hierarchy level 2)
            and_name = self._new_name("and")
            and_hierarchy = 2
            self.nodes[and_name] = {
                "type": "BLOCK",
                "block_type": "AND",
                "inputs": [not_name, subtrahend],
                "output": and_name,
                "hierarchy": and_hierarchy
            }
            
            # Difference bit is A XOR B (hierarchy level 2)
            xor_name = self._new_name("xor")
            xor_hierarchy = 2
            self.nodes[xor_name] = {
                "type": "BLOCK",
                "block_type": "XOR",
                "inputs": [minuend, subtrahend],
                "output": xor_name,
                "hierarchy": xor_hierarchy
            }
            
            # Create the subtractor block that represents this operation
            hierarchy_level = 3  # Higher level than its components
            self.nodes[subtractor_name] = {
                "type": "BLOCK",
                "block_type": "SUBTRACTOR",
                "inputs": [minuend, subtrahend],
                "output": subtractor_name,
                "hierarchy": hierarchy_level,
                "implementation": {
                    "difference": xor_name,
                    "borrow": and_name
                }
            }
            
            # Create a wire from XOR to output for better connection
            wire_name = self._new_name("wire")
            self.nodes[wire_name] = {
                "type": "WIRE",
                "from": xor_name,
                "to": subtractor_name,
                "hierarchy": hierarchy_level
            }
            
            self.max_hierarchy = max(self.max_hierarchy, hierarchy_level)
            
            # Track this output for later connection to destination
            if from_var in self.nodes and self.nodes[from_var]["type"] == "OUTPUT_NODE":
                if from_var not in self.output_connections:
                    self.output_connections[from_var] = []
                self.output_connections[from_var].append(subtractor_name)
                
            return subtractor_name
            
        # Addition handling (using XOR and AND gates)
        elif "+" in expr:
            terms = [t.strip() for t in expr.split("+")]
            adder_name = self._new_name("adder")
            processed_terms = []
            
            # Process each term in the addition
            for term in terms:
                if term.isdigit():
                    const = self.add_constant(int(term))
                    processed_terms.append(const)
                elif "*" in term or "-" in term or any(op in term.lower() for op in logic_ops):
                    # Handle complex terms within addition
                    result = self.process_expr(term, from_var)
                    processed_terms.append(result)
                else:
                    processed_terms.append(term)
            
            # Create XOR gates for sum bits
            current_sum = processed_terms[0]
            xor_hierarchy = 1  # Start with this level
            
            for i in range(1, len(processed_terms)):
                xor_name = self._new_name("xor")
                self.nodes[xor_name] = {
                    "type": "BLOCK",
                    "block_type": "XOR",
                    "inputs": [current_sum, processed_terms[i]],
                    "output": xor_name,
                    "hierarchy": xor_hierarchy
                }
                
                # Create AND gate for carry bit
                and_name = self._new_name("and")
                and_hierarchy = 1  # Same level as XOR
                self.nodes[and_name] = {
                    "type": "BLOCK",
                    "block_type": "AND",
                    "inputs": [current_sum, processed_terms[i]],
                    "output": and_name,
                    "hierarchy": and_hierarchy
                }
                
                # The current sum becomes the XOR result
                current_sum = xor_name
                
                # If this isn't the last term, we need to include the carry in the next iteration
                if i < len(processed_terms) - 1:
                    next_xor_name = self._new_name("xor")
                    next_hierarchy = 2  # Higher than the previous gates
                    self.nodes[next_xor_name] = {
                        "type": "BLOCK",
                        "block_type": "XOR",
                        "inputs": [current_sum, and_name],
                        "output": next_xor_name,
                        "hierarchy": next_hierarchy
                    }
                    current_sum = next_xor_name
            
            # Final adder result
            hierarchy_level = 2  # Set appropriate hierarchy for adder
            self.nodes[adder_name] = {
                "type": "BLOCK",
                "block_type": "ADD",  # Changed from ADDER to ADD
                "inputs": processed_terms,
                "output": adder_name,
                "hierarchy": hierarchy_level
            }
            
            # Create a wire from the final sum to the adder output
            wire_name = self._new_name("wire")
            self.nodes[wire_name] = {
                "type": "WIRE",
                "from": current_sum,
                "to": adder_name,
                "hierarchy": hierarchy_level
            }
            
            self.max_hierarchy = max(self.max_hierarchy, hierarchy_level)
            
            # Track this output for later connection to destination
            if from_var in self.nodes and self.nodes[from_var]["type"] == "OUTPUT_NODE":
                if from_var not in self.output_connections:
                    self.output_connections[from_var] = []
                self.output_connections[from_var].append(adder_name)
                
            return adder_name
            
        # Multiplication handling (simplified)
        elif "*" in expr:
            terms = [t.strip() for t in expr.split("*")]
            mul_name = self._new_name("multiplier")
            inputs = []
            for term in terms:
                if term.isdigit():
                    const = self.add_constant(int(term))
                    inputs.append(const)
                else:
                    # Process complex terms within multiplication
                    processed_term = self.process_expr(term, from_var)
                    inputs.append(processed_term)
            
            hierarchy_level = 1
            self.nodes[mul_name] = {
                "type": "BLOCK",
                "block_type": "MULTIPLIER",
                "inputs": inputs,
                "output": mul_name,
                "hierarchy": hierarchy_level
            }
            self.max_hierarchy = max(self.max_hierarchy, hierarchy_level)
            
            # Track this output for later connection to destination
            if from_var in self.nodes and self.nodes[from_var]["type"] == "OUTPUT_NODE":
                if from_var not in self.output_connections:
                    self.output_connections[from_var] = []
                self.output_connections[from_var].append(mul_name)
                
            return mul_name
            
        elif expr.isdigit():
            return self.add_constant(int(expr))
            
        # Bitwise operations (if not already captured by logic_ops)
        elif "&" in expr and "&&" not in expr:  # Bitwise AND
            terms = [t.strip() for t in expr.split("&")]
            and_name = self._new_name("and")
            inputs = []
            
            for term in terms:
                processed_term = self.process_expr(term, from_var)
                inputs.append(processed_term)
                
            hierarchy_level = 1
            self.nodes[and_name] = {
                "type": "BLOCK",
                "block_type": "AND",
                "inputs": inputs,
                "output": and_name,
                "hierarchy": hierarchy_level
            }
            
            self.max_hierarchy = max(self.max_hierarchy, hierarchy_level)
            
            # Track this output for later connection to destination
            if from_var in self.nodes and self.nodes[from_var]["type"] == "OUTPUT_NODE":
                if from_var not in self.output_connections:
                    self.output_connections[from_var] = []
                self.output_connections[from_var].append(and_name)
                
            return and_name
            
        elif "|" in expr and "||" not in expr:  # Bitwise OR
            terms = [t.strip() for t in expr.split("|")]
            or_name = self._new_name("or")
            inputs = []
            
            for term in terms:
                processed_term = self.process_expr(term, from_var)
                inputs.append(processed_term)
                
            hierarchy_level = 1
            self.nodes[or_name] = {
                "type": "BLOCK",
                "block_type": "OR",
                "inputs": inputs,
                "output": or_name,
                "hierarchy": hierarchy_level
            }
            
            self.max_hierarchy = max(self.max_hierarchy, hierarchy_level)
            
            # Track this output for later connection to destination
            if from_var in self.nodes and self.nodes[from_var]["type"] == "OUTPUT_NODE":
                if from_var not in self.output_connections:
                    self.output_connections[from_var] = []
                self.output_connections[from_var].append(or_name)
                
            return or_name
            
        elif "^" in expr:  # Bitwise XOR
            terms = [t.strip() for t in expr.split("^")]
            xor_name = self._new_name("xor")
            inputs = []
            
            for term in terms:
                processed_term = self.process_expr(term, from_var)
                inputs.append(processed_term)
                
            hierarchy_level = 1
            self.nodes[xor_name] = {
                "type": "BLOCK",
                "block_type": "XOR",
                "inputs": inputs,
                "output": xor_name,
                "hierarchy": hierarchy_level
            }
            
            self.max_hierarchy = max(self.max_hierarchy, hierarchy_level)
            
            # Track this output for later connection to destination
            if from_var in self.nodes and self.nodes[from_var]["type"] == "OUTPUT_NODE":
                if from_var not in self.output_connections:
                    self.output_connections[from_var] = []
                self.output_connections[from_var].append(xor_name)
                
            return xor_name
            
        # Logical operations
        elif "&&" in expr:  # Logical AND
            terms = [t.strip() for t in expr.split("&&")]
            and_name = self._new_name("and")
            inputs = []
            
            for term in terms:
                processed_term = self.process_expr(term, from_var)
                inputs.append(processed_term)
                
            hierarchy_level = 1
            self.nodes[and_name] = {
                "type": "BLOCK",
                "block_type": "AND",
                "inputs": inputs,
                "output": and_name,
                "hierarchy": hierarchy_level
            }
            
            self.max_hierarchy = max(self.max_hierarchy, hierarchy_level)
            
            # Track this output for later connection to destination
            if from_var in self.nodes and self.nodes[from_var]["type"] == "OUTPUT_NODE":
                if from_var not in self.output_connections:
                    self.output_connections[from_var] = []
                self.output_connections[from_var].append(and_name)
                
            return and_name
            
        elif "||" in expr:  # Logical OR
            terms = [t.strip() for t in expr.split("||")]
            or_name = self._new_name("or")
            inputs = []
            
            for term in terms:
                processed_term = self.process_expr(term, from_var)
                inputs.append(processed_term)
                
            hierarchy_level = 1
            self.nodes[or_name] = {
                "type": "BLOCK",
                "block_type": "OR",
                "inputs": inputs,
                "output": or_name,
                "hierarchy": hierarchy_level
            }
            
            self.max_hierarchy = max(self.max_hierarchy, hierarchy_level)
            
            # Track this output for later connection to destination
            if from_var in self.nodes and self.nodes[from_var]["type"] == "OUTPUT_NODE":
                if from_var not in self.output_connections:
                    self.output_connections[from_var] = []
                self.output_connections[from_var].append(or_name)
                
            return or_name
            
        # Unary operations
        elif expr.startswith("~"):  # Bitwise NOT
            operand = expr[1:].strip()
            not_name = self._new_name("not")
            processed_operand = self.process_expr(operand, from_var)
            
            hierarchy_level = 1  # Lowest hierarchy for NOT gate
            self.nodes[not_name] = {
                "type": "BLOCK",
                "block_type": "NOT",
                "inputs": [processed_operand],
                "output": not_name,
                "hierarchy": hierarchy_level
            }
            
            self.max_hierarchy = max(self.max_hierarchy, hierarchy_level)
            
            # Track this output for later connection to destination
            if from_var in self.nodes and self.nodes[from_var]["type"] == "OUTPUT_NODE":
                if from_var not in self.output_connections:
                    self.output_connections[from_var] = []
                self.output_connections[from_var].append(not_name)
                
            return not_name
            
        elif expr.startswith("!"):  # Logical NOT
            operand = expr[1:].strip()
            not_name = self._new_name("not")
            processed_operand = self.process_expr(operand, from_var)
            
            hierarchy_level = 1  # Lowest hierarchy for NOT gate
            self.nodes[not_name] = {
                "type": "BLOCK",
                "block_type": "NOT",
                "inputs": [processed_operand],
                "output": not_name,
                "hierarchy": hierarchy_level
            }
            
            self.max_hierarchy = max(self.max_hierarchy, hierarchy_level)
            
            # Track this output for later connection to destination
            if from_var in self.nodes and self.nodes[from_var]["type"] == "OUTPUT_NODE":
                if from_var not in self.output_connections:
                    self.output_connections[from_var] = []
                self.output_connections[from_var].append(not_name)
                
            return not_name
            
        elif expr.startswith("-") and expr[1:].isdigit():  # Handle negative numbers
            return self.add_constant(-int(expr[1:]))
        elif expr in self.variables:  # Check if it's a variable we've seen before
            return self.variables[expr]
        else:
            # Might be a new variable or a simple identifier
            return expr

    def convert(self, python_code: str):
        self.nodes = {}
        self.variables = {}
        self.output_connections = {}
        self.max_hierarchy = 0
        self.counter = {
            "constant": 0,
            "multiplier": 0,
            "comparator": 0,
            "adder": 0,
            "subtractor": 0,
            "logic": 0,
            "wire": 0,
            "xor": 0,
            "and": 0,
            "or": 0,
            "not": 0,
            "nand": 0,
            "nor": 0,
            "xnor": 0
        }

        lines = python_code.strip().splitlines()
        current_condition = None
        last_var = None
        condition_blocks = {}  # Store info about if-elif-else blocks

        # First pass: identify input and output nodes
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            if " = input()" in stripped:
                var = stripped.split("=")[0].strip()
                self.nodes[var] = {
                    "type": "INPUT_NODE",
                    "hierarchy": 0
                }

            elif " = output()" in stripped:
                var = stripped.split("=")[0].strip()
                # We'll update the hierarchy for outputs later
                self.nodes[var] = {
                    "type": "OUTPUT_NODE",
                    "hierarchy": 0,  # Placeholder, will be updated later
                    "inputs": []     # Will track nodes connected to this output
                }

        # Second pass: process all expressions and blocks
        for line in lines:
            stripped = line.strip()

            if not stripped:
                continue

            # Skip input/output declarations we already processed
            if " = input()" in stripped or " = output()" in stripped:
                continue

            elif stripped.startswith("if ") or stripped.startswith("elif "):
                condition = stripped.split(' ', 1)[1].rstrip(":")
                current_condition = self.simplify_condition(condition)
                
                # Create a new condition block
                if stripped.startswith("if "):
                    condition_blocks = {"if": current_condition, "branches": {}}
                else:  # elif
                    condition_blocks["branches"][current_condition] = None

            elif stripped.startswith("else:"):
                current_condition = "default"
                condition_blocks["branches"]["default"] = None

            elif "=" in stripped and not stripped.startswith("#"):  # Ignore comments
                var, expr = map(str.strip, stripped.split("=", 1))
                expr_result = self.process_expr(expr, var)
                wire_hierarchy = self.max_hierarchy + 1

                # Store this assignment as a variable
                self.variables[var] = expr_result
                
                # If the destination is an output node, update its inputs list
                if var in self.nodes and self.nodes[var]["type"] == "OUTPUT_NODE":
                    if not hasattr(self.nodes[var], "inputs"):
                        self.nodes[var]["inputs"] = []
                    self.nodes[var]["inputs"].append(expr_result)

                if current_condition == "default" or current_condition is None:
                    wire_name = self._new_name("wire")
                    self.nodes[wire_name] = {
                        "type": "WIRE",
                        "from": expr_result,
                        "to": var,
                        "hierarchy": wire_hierarchy
                    }
                    self.max_hierarchy = max(self.max_hierarchy, wire_hierarchy)
                    
                    # Store this branch result if part of a condition block
                    if current_condition == "default" and condition_blocks:
                        condition_blocks["branches"]["default"] = expr_result
                else:
                    # Store this branch result
                    if condition_blocks:
                        if current_condition == condition_blocks["if"]:
                            condition_blocks["if_result"] = expr_result
                        else:
                            condition_blocks["branches"][current_condition] = expr_result
                    
                    comp_name = self._new_name("comparator")
                    comp_hierarchy = self.max_hierarchy + 1
                    self.nodes[comp_name] = {
                        "type": "BLOCK",
                        "block_type": "COMPARATOR",
                        "condition": current_condition,
                        "true_path": expr_result,
                        "false_path": None,  # Will be updated if this is part of an if-else
                        "output": var,
                        "hierarchy": comp_hierarchy
                    }
                    self.max_hierarchy = max(self.max_hierarchy, comp_hierarchy)

        # Update all output nodes to have the highest hierarchy
        output_hierarchy = self.max_hierarchy + 1
        for node_name, node in self.nodes.items():
            if node["type"] == "OUTPUT_NODE":
                node["hierarchy"] = output_hierarchy

        # Create connections for all outputs
        for output_name, connected_nodes in self.output_connections.items():
            if output_name in self.nodes and self.nodes[output_name]["type"] == "OUTPUT_NODE":
                for node in connected_nodes:
                    wire_name = self._new_name("wire")
                    self.nodes[wire_name] = {
                        "type": "WIRE",
                        "from": node,
                        "to": output_name,
                        "hierarchy": self.nodes[output_name]["hierarchy"] - 1
                    }

        return self.nodes