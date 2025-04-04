import pickle
import ast
import re

class PseudocodeParser:
    def __init__(self):
        self.expressions = {}
        self.variable_map = {}

    def parse_pseudocode(self, pseudocode):
        """Convert pseudocode into structured logical expressions"""
        lines = pseudocode.strip().split('\n')
        
        for line in lines:
            line = line.strip().lower()
            if not line or line.startswith('#'):  # Skip empty lines and comments
                continue
                
            # Handle variable assignments without comparisons
            if '=' in line and not any(op in line for op in ['<', '>', '<=', '>=', '==', '!=']) and not any(op in line for op in ['and', 'or', 'not']):
                var, value = self._parse_assignment(line)
                self.variable_map[var] = value
                
            # Handle conditions and logical operations
            else:
                self._parse_logical_line(line)

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

    def _parse_logical_line(self, line):
        """Parse logical operations and conditions into structured format"""
        if line.startswith('if'):
            line = line.replace('if ', '').replace('then', '').strip()

        # Handle assignments with expressions
        if '=' in line:
            output_var, expression = line.split('=', 1)
            output_var = output_var.strip()
            line = expression.strip()
        else:
            output_var = None

        # Parse nested expressions with parentheses
        def parse_expression(expr):
            expr = expr.strip()
            # Check for parentheses to handle nesting
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
            else:
                # Comparison operators
                comparison_ops = {'<': 'less_than', '>': 'greater_than', '<=': 'less_equal',
                                '>=': 'greater_equal', '==': 'equal', '!=': 'not_equal'}
                for op, op_name in comparison_ops.items():
                    if op in expr:
                        return {
                            'type': 'condition',
                            'input': set(re.findall(r'[a-zA-Z0-9.]+', expr)),
                            'operator': op
                        }
                # If no operators, assume it's a variable or value
                return {'type': 'value', 'input': {expr.strip()}}

            # Recursively parse sub-expressions
            sub_expressions = [parse_expression(part) for part in parts]
            return {
                'type': op_type,
                'input': set().union(*[sub['input'] for sub in sub_expressions]),
                'sub_expressions': sub_expressions
            }

        # Parse the line
        parsed_expr = parse_expression(line)
        inputs = parsed_expr.get('input', set())
        outputs = {output_var} if output_var else {f'exp_{len(self.expressions)}'}

        # Structure the expression
        key = next(iter(outputs))
        self.expressions[key] = {
            'type': parsed_expr['type'],
            'input': inputs,
            'output': outputs,
            'operator': parsed_expr.get('operator'),
            'sub_expressions': parsed_expr.get('sub_expressions', [])
        }

    def evaluate_expression(self, key):
        """Evaluate the boolean value of an expression using variable_map"""
        expr = self.expressions.get(key)
        if not expr:
            return None

        def eval_sub(expr_dict):
            if expr_dict['type'] == 'value':
                value = next(iter(expr_dict['input']))
                return self.variable_map.get(value, value) if value in self.variable_map else value
            elif expr_dict['type'] == 'condition':
                left, right = list(expr_dict['input'])
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
            return False

        result = eval_sub(expr)
        if key in self.variable_map:
            self.variable_map[key] = result
        return result

    def to_pickle(self, filename):
        """Save the expressions and variable map to a pickle file"""
        data = {
            'expressions': self.expressions,
            'variables': self.variable_map
        }
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    @staticmethod
    def from_pickle(filename):
        """Load logical expressions from pickle file"""
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        converter = PseudocodeParser()
        converter.expressions = data['expressions']
        converter.variable_map = data['variables']
        return converter

# Example usage
# if __name__ == "__main__":
#     # Sample pseudocode with nested expressions
#     sample_pseudocode = """
#     x = 10
#     y = 20
#     z = 30
#     IF (x < y) and (z > 10) THEN
#     b = y < z
#     c = (x < y) or (z == 15)
#     """

#     # Convert pseudocode
#     converter = PseudocodeConverter()
#     result = converter.parse_pseudocode(sample_pseudocode)
#     print("Expressions:", result)
#     print("Variables:", converter.variable_map)

#     # Evaluate expressions
#     for key in result:
#         print(f"Evaluating {key}: {converter.evaluate_expression(key)}")

#     # Save to pickle
#     converter.to_pickle('logic_expression.pkl')

#     # Load from pickle
#     loaded_converter = PseudocodeConverter.from_pickle('logic_expression.pkl')
#     print("\nLoaded from pickle:")
#     print("Expressions:", loaded_converter.expressions)
#     print("Variables:", loaded_converter.variable_map)
#     for key in loaded_converter.expressions:
#         print(f"Evaluating {key}: {loaded_converter.evaluate_expression(key)}")