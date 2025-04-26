class BooleanAlgebraConverter:
    """Converts AST to Boolean algebra expressions"""
    
    def __init__(self):
        # Map built-in functions to their Boolean algebra operations
        self.op_map = {
            (lambda x, y: x and y): "·",  # Logical AND
            (lambda x, y: x or y): "+",   # Logical OR
        }
        
        # Comparisons will need to be represented as variables
        self.comp_ops = {
            (lambda x, y: x < y): "<",
            (lambda x, y: x > y): ">",
            (lambda x, y: x == y): "=",
            (lambda x, y: x != y): "≠",
            (lambda x, y: x <= y): "≤",
            (lambda x, y: x >= y): "≥",
        }
    
    def convert_ast_to_boolean(self, ast):
        """Convert AST to Boolean algebra expression"""
        if ast.data == 'start':
            rule_data = ast.children[0]
            
            # Process the statements to find conditional blocks
            for statement in rule_data.get('statements', []):
                if hasattr(statement, 'data') and statement.data == 'statement':
                    statement_dict = statement.children[0]
                    if statement_dict.get('type') == 'conditional_block':
                        # This is where our conditional logic is
                        return self._process_conditional_block(statement_dict)
                    elif statement_dict.get('type') == 'assign':
                        # Handle assignment statement
                        var = statement_dict.get('var')
                        expr = statement_dict.get('expr')
                        expr_value = self._extract_value(expr)
                        return f"{var} = {expr_value}"
        
        return "No conditional logic found"
    
    def _process_conditional_block(self, conditional_block):
        """Process conditional block into Boolean algebra expression"""
        parts = conditional_block.get('parts', [])
        
        # For each condition, we'll create a Boolean term
        # Then we'll combine these terms based on the logic
        
        # First, extract all conditions and their corresponding output assignments
        conditions_and_outputs = []
        
        for part in parts:
            if part.get('type') in ['if', 'elif']:
                condition = part.get('condition')
                block = part.get('block')
                
                # Convert condition to Boolean expression
                bool_expr = self._convert_condition_to_boolean(condition)
                
                # Extract the output assignment
                output_value = self._extract_output_value(block)
                
                conditions_and_outputs.append((bool_expr, output_value))
            
            elif part.get('type') == 'else':
                # Else condition is the negation of all previous conditions
                block = part.get('block')
                output_value = self._extract_output_value(block)
                conditions_and_outputs.append(("else", output_value))
        
        # Now convert to a Boolean function representation
        return self._create_boolean_function(conditions_and_outputs)
    
    def _convert_condition_to_boolean(self, condition):
        """Convert a single condition to Boolean algebra notation"""
        if isinstance(condition, dict):
            if 'op' in condition:
                # Binary operation
                if 'left' in condition and 'right' in condition:
                    left = self._convert_condition_to_boolean(condition['left'])
                    right = self._convert_condition_to_boolean(condition['right'])
                    
                    op = condition['op']
                    
                    # Handle logical operations (AND, OR)
                    if op in self.op_map or op.__name__ in ['and_', 'or_']:
                        op_symbol = self.op_map.get(op, "·" if op.__name__ == 'and_' else "+")
                        return f"({left} {op_symbol} {right})"
                    
                    # Handle comparison operations (create Boolean variables)
                    elif op in self.comp_ops or op.__name__ in ['lt', 'gt', 'eq', 'ne', 'le', 'ge']:
                        op_name = op.__name__ if hasattr(op, '__name__') else str(op)
                        
                        # Extract variable names and values
                        left_var = self._extract_var_name(condition['left'])
                        right_val = self._extract_value(condition['right'])
                        
                        # Create a Boolean variable name representing this comparison
                        if op_name == 'lt' or op == self.comp_ops.get((lambda x, y: x < y)):
                            return f"{left_var}<{right_val}"
                        elif op_name == 'gt' or op == self.comp_ops.get((lambda x, y: x > y)):
                            return f"{left_var}>{right_val}"
                        else:
                            # For other comparisons, create generic variable
                            return f"{left_var}{self._get_comp_symbol(op)}{right_val}"
        
        # Default case
        return str(condition)
    
    def _get_comp_symbol(self, op):
        """Get the symbol for a comparison operator"""
        if op.__name__ == 'lt':
            return "<"
        elif op.__name__ == 'gt':
            return ">"
        elif op.__name__ == 'eq':
            return "="
        elif op.__name__ == 'ne':
            return "≠"
        elif op.__name__ == 'le':
            return "≤"
        elif op.__name__ == 'ge':
            return "≥"
        return str(op)
    
    def _extract_var_name(self, node):
        """Extract variable name from node"""
        if hasattr(node, 'data') and node.data == 'atom':
            if len(node.children) > 0:
                return str(node.children[0])
        return str(node)
    
    def _extract_value(self, node):
        """Extract value from node"""
        if hasattr(node, 'data') and node.data == 'atom':
            if len(node.children) > 0:
                return str(node.children[0])
        elif isinstance(node, dict) and 'op' in node and node['op'] == '-':
            # Handle negative values
            if 'arg' in node and hasattr(node['arg'], 'data') and node['arg'].data == 'atom':
                return f"-{node['arg'].children[0]}"
        return str(node)
    
    def _extract_output_value(self, block):
        """Extract the output value from a block"""
        if hasattr(block, 'data') and block.data == 'block':
            for stmt in block.children:
                if hasattr(stmt, 'data') and stmt.data == 'statement':
                    stmt_dict = stmt.children[0]
                    if stmt_dict.get('type') == 'assign':
                        var = stmt_dict.get('var')
                        expr = stmt_dict.get('expr')
                        
                        # Extract the assigned value
                        if hasattr(expr, 'data') and expr.data == 'atom':
                            if len(expr.children) > 0:
                                return str(expr.children[0])
                        elif isinstance(expr, dict) and 'op' in expr and expr['op'] == '-':
                            # Handle negative values
                            if 'arg' in expr and hasattr(expr['arg'], 'data') and expr['arg'].data == 'atom':
                                return f"-{expr['arg'].children[0]}"
        return "unknown"
    
    def _create_boolean_function(self, conditions_and_outputs):
        """Create a Boolean function from conditions and outputs"""
        # Group by output values
        output_groups = {}
        
        for condition, output in conditions_and_outputs:
            if output not in output_groups:
                output_groups[output] = []
            
            if condition != "else":
                output_groups[output].append(condition)
            else:
                # Handle else condition as the negation of all other conditions
                other_conditions = [c for c, _ in conditions_and_outputs if c != "else"]
                if other_conditions:
                    not_conditions = [f"¬({c})" for c in other_conditions]
                    combined = " · ".join(not_conditions)
                    output_groups[output].append(combined)
        
        # Now combine to create the Boolean function
        boolean_expressions = []
        
        for output_val, conditions in output_groups.items():
            if conditions:
                # If there are multiple conditions for this output, OR them together
                if len(conditions) > 1:
                    combined_condition = " + ".join([f"({c})" for c in conditions])
                else:
                    combined_condition = conditions[0]
                
                boolean_expressions.append(f"{combined_condition} → uk={output_val}")
        
        # Join all expressions
        return " | ".join(boolean_expressions)


class Tree:
    """Simple Tree class to mimic the AST structure"""
    def __init__(self, data, children):
        self.data = data
        self.children = children


class Token:
    """Simple Token class to mimic the AST structure"""
    def __init__(self, type, value):
        self.type = type
        self.value = value
