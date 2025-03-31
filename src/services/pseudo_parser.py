import json
import ast
import re

class PseudocodeParser:
    def __init__(self):
        self.expressions = {}
        self.variable_map = {}

    def parse_pseudocode(self, pseudocode: str):
        """Convert pseudocode into structured logical expressions"""
        self.expressions = {}
        self.variable_map = {}
        lines = pseudocode.strip().split('\n')
        
        for line in lines:
            line = line.strip().lower()
            if not line or line.startswith('#'):  # Skip empty lines and comments
                continue
                
            # Handle simple variable assignments (e.g., x = 10)
            if '=' in line and not any(op in line for op in ['<', '>', '<=', '>=', '==', '!=', 'and', 'or', 'not', '+', '-', '*', '/']):
                var, value = self._parse_assignment(line)
                self.variable_map[var] = value
                
            # Handle conditionals, logical ops, or arithmetic
            else:
                self._parse_operation_line(line)

        return self.expressions

    def _parse_assignment(self, line):
        """Parse simple variable assignments"""
        var, value = line.split('=', 1)
        var = var.strip()
        value = value.strip()
        try:
            value = ast.literal_eval(value)
        except:
            value = value.strip("'").strip('"')
        return var, value

    def _parse_operation_line(self, line):
        """Parse conditionals, logical operations, and arithmetic"""
        if line.startswith('if'):
            line = line.replace('if ', '').replace('then', '').strip()

        # Handle assignments (e.g., b = x < y)
        if '=' in line:
            output_var, expression = line.split('=', 1)
            output_var = output_var.strip()
            expression = expression.strip()
        else:
            output_var = f'exp_{len(self.expressions)}'
            expression = line

        # Parse nested expressions with parentheses
        def parse_expression(expr):
            expr = expr.strip()
            # Handle parentheses for nested expressions
            if expr.startswith('(') and expr.endswith(')'):
                expr = expr[1:-1]
                return parse_expression(expr)

            # Logical operators
            if ' and ' in expr:
                op_type = 'and'
                parts = re.split(r'\s+and\s+', expr)
            elif ' or ' in expr:
                op_type = 'or'
                parts = re.split(r'\s+or\s+', expr)
            elif 'not ' in expr:
                op_type = 'not'
                parts = [expr.replace('not ', '').strip()]
            # Arithmetic operators
            elif '+' in expr:
                op_type = 'add'
                parts = expr.split('+')
            elif '-' in expr:
                op_type = 'subtract'
                parts = expr.split('-')
            elif '*' in expr:
                op_type = 'multiply'
                parts = expr.split('*')
            elif '/' in expr:
                op_type = 'divide'
                parts = expr.split('/')
            else:
                # Comparison operators
                comparison_ops = {'<': 'less_than', '>': 'greater_than', '<=': 'less_equal',
                                 '>=': 'greater_equal', '==': 'equal', '!=': 'not_equal'}
                for op, op_name in comparison_ops.items():
                    if op in expr:
                        inputs = set(re.findall(r'[a-zA-Z0-9.]+', expr))
                        return {
                            'type': 'condition',
                            'input': list(inputs),  # Convert set to list
                            'operator': op
                        }
                # If no operators, assume it's a variable or value
                return {'type': 'value', 'input': [expr.strip()]}  # Store as list

            # Recursively parse sub-expressions
            sub_expressions = [parse_expression(part) for part in parts]
            inputs = set().union(*[set(sub['input']) for sub in sub_expressions])
            return {
                'type': op_type,
                'input': list(inputs),  # Convert set to list
                'sub_expressions': sub_expressions
            }

        # Parse the expression
        parsed_expr = parse_expression(expression)
        outputs = {output_var}

        # Structure the expression
        self.expressions[output_var] = {
            'type': parsed_expr['type'],
            'input': parsed_expr.get('input', []),  # Already a list
            'output': list(outputs),  # Convert set to list
            'operator': parsed_expr.get('operator'),
            'sub_expressions': parsed_expr.get('sub_expressions', [])
        }

    def evaluate_expression(self, key):
        """Evaluate the expression (conditionals or arithmetic)"""
        expr = self.expressions.get(key)
        if not expr:
            return None

        def eval_sub(expr_dict):
            if expr_dict['type'] == 'value':
                value = expr_dict['input'][0]  # Now a list
                return self.variable_map.get(value, float(value) if value.replace('.', '').isdigit() else value)
            elif expr_dict['type'] == 'condition':
                left, right = expr_dict['input']  # Now a list
                left_val = self.variable_map.get(left, float(left) if left.replace('.', '').isdigit() else left)
                right_val = self.variable_map.get(right, float(right) if right.replace('.', '').isdigit() else right)
                if expr_dict['operator'] == '<':
                    return left_val < right_val
                elif expr_dict['operator'] == '>':
                    return left_val > right_val
                elif expr_dict['operator'] == '<=':
                    return left_val <= right_val
                elif expr_dict['operator'] == '>=':
                    return left_val >= right_val
                elif expr_dict['operator'] == '==':
                    return left_val == right_val
                elif expr_dict['operator'] == '!=':
                    return left_val != right_val
            elif expr_dict['type'] == 'and':
                return all(eval_sub(sub) for sub in expr_dict['sub_expressions'])
            elif expr_dict['type'] == 'or':
                return any(eval_sub(sub) for sub in expr_dict['sub_expressions'])
            elif expr_dict['type'] == 'not':
                return not eval_sub(expr_dict['sub_expressions'][0])
            elif expr_dict['type'] == 'add':
                values = [eval_sub(sub) for sub in expr_dict['sub_expressions']]
                return sum(values)
            elif expr_dict['type'] == 'subtract':
                values = [eval_sub(sub) for sub in expr_dict['sub_expressions']]
                return values[0] - values[1]
            elif expr_dict['type'] == 'multiply':
                values = [eval_sub(sub) for sub in expr_dict['sub_expressions']]
                result = 1
                for val in values:
                    result *= val
                return result
            elif expr_dict['type'] == 'divide':
                values = [eval_sub(sub) for sub in expr_dict['sub_expressions']]
                return values[0] / values[1] if values[1] != 0 else float('inf')
            return None

        result = eval_sub(expr)
        if key in self.variable_map:
            self.variable_map[key] = result
        return result

    def to_json(self, filename):
        """Save the expressions and variable map to a JSON file"""
        data = {
            'expressions': self.expressions,
            'variables': self.variable_map
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def from_json(filename):
        """Load logical expressions from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        converter = PseudocodeParser()
        converter.expressions = data['expressions']
        converter.variable_map = data['variables']
        return converter

# # Example usage
if __name__ == "__main__":
    # Sample pseudocode with conditionals and arithmetic
    sample_pseudocode = """
    INPUT INTEGER x
    OUTPUT BOOLEAN Y

    if x < 10:
        Y = X
    else:
        Y = 0     
    """

    # Convert pseudocode
    converter = PseudocodeParser()
    result = converter.parse_pseudocode(sample_pseudocode)
    print("Expressions:", result)
    print("Variables (initial):", converter.variable_map)

    # Evaluate expressions
    for key in result:
        print(f"Evaluating {key}: {converter.evaluate_expression(key)}")

    print("Variables (final):", converter.variable_map)

    # Save to JSON
    converter.to_json('logic_expression.json')

    # Load from JSON
    loaded_converter = PseudocodeParser.from_json('logic_expression.json')
    print("\nLoaded from JSON:")
    print("Expressions:", loaded_converter.expressions)
    print("Variables:", loaded_converter.variable_map)
    for key in loaded_converter.expressions:
        print(f"Evaluating {key}: {loaded_converter.evaluate_expression(key)}")