from lark import Tree, Token
from dataclasses import dataclass
from typing import List, Any, Optional, Set, Tuple
from enum import Enum, auto

# Define rule types
class RuleType(Enum):
    START = "start"
    STATEMENT = "statement"
    BLOCK = "block"
    ATOM = "atom"

# Define statement types
class StatementType(Enum):
    INPUT_DECL = "input_decl"
    OUTPUT_DECL = "output_decl"
    ASSIGN = "assign"
    CONDITIONAL_BLOCK = "conditional_block"

# Define conditional part types
class ConditionalPartType(Enum):
    IF = "if"
    ELIF = "elif"
    ELSE = "else"

# Define validation error
@dataclass
class ValidationError:
    message: str
    node: Optional[Any] = None

class ASTValidator:
    def __init__(self):
        # Valid binary operators (using string names or callable names)
        self.valid_operators = {
            'lt', 'gt', 'le', 'ge', 'eq', 'ne', 'and_', 'or_',
            'add', 'sub', 'mul', 'div', 'mod'
        }
        # Valid unary operators
        self.valid_unary_operators = {'sub', '-'}  # Include '-' for unary minus
        # Node specifications
        self.node_specs = {
            RuleType.START: {
                'required': ['inputs', 'outputs', 'variables', 'statements'],
                'checks': [
                    lambda node: isinstance(node['inputs'], list) and all(isinstance(v, str) for v in node['inputs']),
                    lambda node: isinstance(node['outputs'], list) and all(isinstance(v, str) for v in node['outputs']),
                    lambda node: isinstance(node['variables'], set) and all(isinstance(v, str) for v in node['variables']),
                    lambda node: isinstance(node['statements'], list) and all(isinstance(s, Tree) and s.data == RuleType.STATEMENT.value for s in node['statements'])
                ]
            },
            RuleType.STATEMENT: {
                'required': ['type'],
                'valid_types': {t.value for t in StatementType},
                'checks': []
            },
            RuleType.BLOCK: {
                'required': [],
                'checks': [
                    lambda node: all(isinstance(s, Tree) and s.data == RuleType.STATEMENT.value for s in node.children)
                ]
            },
            RuleType.ATOM: {
                'required': [],
                'checks': []  # We'll handle atom validation separately
            }
        }

    def validate(self, ast: Tree) -> Tuple[bool, str]:
        """Validate the AST and return True if valid, False otherwise."""
        mistakes = []
        # First check basic structure
        if not isinstance(ast, Tree) or ast.data != RuleType.START.value:
            mistakes.append("Validation Error: Root node must be a Tree with START rule")
            return False, mistakes
            
        if len(ast.children) != 1 or not isinstance(ast.children[0], dict):
            mistakes.append("Validation Error: START node must have exactly one dictionary child")
            return False, mistakes
            
        # Extract declared variables (inputs and outputs)
        root_dict = ast.children[0]
        inputs = set(root_dict.get('inputs', []))
        outputs = set(root_dict.get('outputs', []))
        declared_variables = inputs.union(outputs)
        
        # Check that all variables in 'variables' set are properly declared
        all_variables = root_dict.get('variables', set())
        undeclared = all_variables - declared_variables
        if undeclared:
            for var in undeclared:
                mistakes.append(f"Validation Error: Variable '{var}' is in variables set but not declared as input or output")
            
            return False, mistakes
        
        # Now perform deeper validation with proper declared variables
        errors = self._validate_tree(ast, declared_variables, inputs)
        if errors:
            for error in errors:
                mistakes.append(f"Validation Error: {error.message}")
            return False, mistakes
        return True, None

    def _validate_tree(self, node: Tree, variables: Set[str], input_vars: Set[str]) -> List[ValidationError]:
        """Recursively validate the AST."""
        errors = []

        if not isinstance(node, Tree):
            return [ValidationError("Node must be a Tree", node)]

        # Check node type
        node_label = node.data
        try:
            rule_type = RuleType(node_label)
        except ValueError:
            return [ValidationError(f"Invalid rule type: {node_label}", node)]

        # Handle START node
        if rule_type == RuleType.START:
            if len(node.children) != 1 or not isinstance(node.children[0], dict):
                errors.append(ValidationError("START node must have exactly one dictionary child", node))
                return errors
            node_dict = node.children[0]
            spec = self.node_specs[rule_type]
            
            # Check required fields
            for field in spec['required']:
                if field not in node_dict:
                    errors.append(ValidationError(f"Missing required field '{field}' in {rule_type.name}", node))
            
            # Run custom checks
            for check in spec['checks']:
                try:
                    if not check(node_dict):
                        errors.append(ValidationError(f"Validation check failed for {rule_type.name}", node))
                except Exception as e:
                    errors.append(ValidationError(f"Validation check error for {rule_type.name}: {str(e)}", node))
            
            # Validate statements
            for stmt in node_dict.get('statements', []):
                errors.extend(self._validate_tree(stmt, variables, input_vars))
        
        # Handle STATEMENT node
        elif rule_type == RuleType.STATEMENT:
            if len(node.children) != 1 or not isinstance(node.children[0], dict):
                errors.append(ValidationError("STATEMENT node must have exactly one dictionary child", node))
                return errors
            stmt_dict = node.children[0]
            spec = self.node_specs[rule_type]
            
            # Check statement type
            stmt_type = stmt_dict.get('type')
            if stmt_type not in spec['valid_types']:
                errors.append(ValidationError(f"Invalid statement type: {stmt_type}", node))
                return errors
            
            # Validate specific statement types
            if stmt_type == StatementType.INPUT_DECL.value or stmt_type == StatementType.OUTPUT_DECL.value:
                if 'vars' not in stmt_dict:
                    errors.append(ValidationError(f"{stmt_type} missing 'vars' field", node))
                else:
                    for var in stmt_dict['vars']:
                        if var not in variables:
                            errors.append(ValidationError(f"Variable '{var}' in {stmt_type} not declared as input or output", node))
            
            elif stmt_type == StatementType.ASSIGN.value:
                if 'var' not in stmt_dict or 'expr' not in stmt_dict:
                    errors.append(ValidationError("Assign statement missing 'var' or 'expr'", node))
                else:
                    var_name = stmt_dict['var']
                    if var_name not in variables:
                        errors.append(ValidationError(f"Assigned variable '{var_name}' not declared as input or output", node))
                    # Check if trying to assign to an input variable
                    elif var_name in input_vars:
                        errors.append(ValidationError(f"Cannot assign to input variable '{var_name}'", node))
                    errors.extend(self._validate_expression(stmt_dict['expr'], variables, input_vars))
            
            elif stmt_type == StatementType.CONDITIONAL_BLOCK.value:
                if 'parts' not in stmt_dict or not stmt_dict['parts']:
                    errors.append(ValidationError("Conditional block missing or empty 'parts'", node))
                else:
                    has_if = False
                    for part in stmt_dict['parts']:
                        part_type = part.get('type')
                        if part_type not in {t.value for t in ConditionalPartType}:
                            errors.append(ValidationError(f"Invalid conditional part type: {part_type}", node))
                        if part_type == ConditionalPartType.IF.value:
                            has_if = True
                        if part_type in {ConditionalPartType.IF.value, ConditionalPartType.ELIF.value}:
                            if 'condition' not in part or 'block' not in part:
                                errors.append(ValidationError(f"{part_type} missing 'condition' or 'block'", node))
                            else:
                                errors.extend(self._validate_condition(part['condition'], variables, input_vars))
                                if isinstance(part['block'], Tree):
                                    errors.extend(self._validate_tree(part['block'], variables, input_vars))
                        elif part_type == ConditionalPartType.ELSE.value:
                            if 'block' not in part:
                                errors.append(ValidationError("Else missing 'block'", node))
                            elif isinstance(part['block'], Tree):
                                errors.extend(self._validate_tree(part['block'], variables, input_vars))
                    if not has_if:
                        errors.append(ValidationError("Conditional block missing 'if' part", node))
        
        # Handle BLOCK node
        elif rule_type == RuleType.BLOCK:
            spec = self.node_specs[rule_type]
            for check in spec['checks']:
                try:
                    if not check(node):
                        errors.append(ValidationError("Block validation failed", node))
                except Exception as e:
                    errors.append(ValidationError(f"Block validation error: {str(e)}", node))
            for stmt in node.children:
                errors.extend(self._validate_tree(stmt, variables, input_vars))
        
        # Handle ATOM node
        elif rule_type == RuleType.ATOM:
            if not node.children or len(node.children) != 1:
                errors.append(ValidationError("Atom must have exactly one child", node))
            else:
                value = node.children[0]
                # Check if the value is a variable (string) and if it's declared
                if isinstance(value, str) and value not in variables:
                    errors.append(ValidationError(f"Undeclared variable '{value}' in atom", node))
                # No need to validate literals (non-string values)
        
        return errors

    def _validate_condition(self, condition: dict, variables: Set[str], input_vars: Set[str]) -> List[ValidationError]:
        """Validate a condition in a conditional block."""
        errors = []
        if not isinstance(condition, dict) or 'op' not in condition:
            errors.append(ValidationError("Condition must be a dictionary with 'op'", condition))
            return errors
        
        # Handle operator (callable or string)
        op = condition['op'].__name__ if callable(condition['op']) else condition['op']
        
        # Check if operator is unary or binary
        if op in self.valid_unary_operators:
            if 'arg' not in condition:
                errors.append(ValidationError("Unary operation missing 'arg'", condition))
            else:
                if isinstance(condition['arg'], Tree):
                    errors.extend(self._validate_tree(condition['arg'], variables, input_vars))
                elif isinstance(condition['arg'], dict):
                    errors.extend(self._validate_expression(condition['arg'], variables, input_vars))
                else:
                    errors.append(ValidationError(f"Invalid argument for unary operation: {condition['arg']}", condition))
        elif op in self.valid_operators:
            if 'left' not in condition or 'right' not in condition:
                errors.append(ValidationError("Binary operation missing 'left' or 'right'", condition))
            else:
                # Validate left operand
                if isinstance(condition['left'], Tree):
                    errors.extend(self._validate_tree(condition['left'], variables, input_vars))
                elif isinstance(condition['left'], dict):
                    errors.extend(self._validate_condition(condition['left'], variables, input_vars))
                else:
                    errors.append(ValidationError(f"Invalid left operand: {condition['left']}", condition))
                
                # Validate right operand
                if isinstance(condition['right'], Tree):
                    errors.extend(self._validate_tree(condition['right'], variables, input_vars))
                elif isinstance(condition['right'], dict):
                    errors.extend(self._validate_condition(condition['right'], variables, input_vars))
                else:
                    errors.append(ValidationError(f"Invalid right operand: {condition['right']}", condition))
        else:
            errors.append(ValidationError(f"Invalid operator: {op}", condition))
        
        return errors

    def _validate_expression(self, expr: Any, variables: Set[str], input_vars: Set[str]) -> List[ValidationError]:
        """Validate an expression (atom or operation)."""
        errors = []
        if isinstance(expr, Tree):
            errors.extend(self._validate_tree(expr, variables, input_vars))
        elif isinstance(expr, dict) and 'op' in expr:
            op = expr['op'].__name__ if callable(expr['op']) else expr['op']
            if op in self.valid_unary_operators:
                if 'arg' not in expr:
                    errors.append(ValidationError("Unary operation missing 'arg'", expr))
                else:
                    if isinstance(expr['arg'], Tree):
                        errors.extend(self._validate_tree(expr['arg'], variables, input_vars))
                    elif isinstance(expr['arg'], dict):
                        errors.extend(self._validate_expression(expr['arg'], variables, input_vars))
                    else:
                        errors.append(ValidationError(f"Invalid argument for unary operation: {expr['arg']}", expr))
            elif op in self.valid_operators:
                if 'left' not in expr or 'right' not in expr:
                    errors.append(ValidationError("Binary operation missing 'left' or 'right'", expr))
                else:
                    # Validate left operand
                    if isinstance(expr['left'], Tree):
                        errors.extend(self._validate_tree(expr['left'], variables, input_vars))
                    elif isinstance(expr['left'], dict):
                        errors.extend(self._validate_expression(expr['left'], variables, input_vars))
                    else:
                        errors.append(ValidationError(f"Invalid left operand: {expr['left']}", expr))
                    
                    # Validate right operand
                    if isinstance(expr['right'], Tree):
                        errors.extend(self._validate_tree(expr['right'], variables, input_vars))
                    elif isinstance(expr['right'], dict):
                        errors.extend(self._validate_expression(expr['right'], variables, input_vars))
                    else:
                        errors.append(ValidationError(f"Invalid right operand: {expr['right']}", expr))
            else:
                errors.append(ValidationError(f"Invalid operator: {op}", expr))
        else:
            errors.append(ValidationError(f"Invalid expression: must be an atom or operation, got {expr}", expr))
        return errors

# # Example usage
# if __name__ == "__main__":
#     from lark import Tree, Token
#     import operator

#     # AST with undeclared variables and attempt to assign to input
#     sample_ast = Tree(Token('RULE', 'start'), [{
#         'inputs': ['ok'],
#         'outputs': ['uk'],
#         'variables': {'ok', 'uk', 'our', 'key'},  # 'our' and 'key' are in variables but not declared as inputs/outputs
#         'statements': [
#             Tree(Token('RULE', 'statement'), [{'type': 'input_decl', 'vars': ['ok']}]),
#             Tree(Token('RULE', 'statement'), [{'type': 'output_decl', 'vars': ['uk']}]),
#             Tree(Token('RULE', 'statement'), [{
#                 'type': 'assign',
#                 'var': 'ok',  # Attempting to assign to input variable!
#                 'expr': Tree(Token('RULE', 'atom'), [5.0])
#             }]),
#             Tree(Token('RULE', 'statement'), [{
#                 'type': 'conditional_block',
#                 'parts': [
#                     {
#                         'type': 'if',
#                         'condition': {
#                             'op': operator.and_,
#                             'left': {
#                                 'op': operator.lt,
#                                 'left': Tree(Token('RULE', 'atom'), ['ok']),
#                                 'right': Tree(Token('RULE', 'atom'), [10.0])
#                             },
#                             'right': {
#                                 'op': operator.gt,
#                                 'left': Tree(Token('RULE', 'atom'), ['ok']),
#                                 'right': Tree(Token('RULE', 'atom'), [0.0])
#                             }
#                         },
#                         'block': Tree(Token('RULE', 'block'), [
#                             Tree(Token('RULE', 'statement'), [{
#                                 'type': 'assign',
#                                 'var': 'uk',
#                                 'expr': Tree(Token('RULE', 'atom'), [10.0])
#                             }])
#                         ])
#                     },
#                     {
#                         'type': 'elif',
#                         'condition': {
#                             'op': operator.and_,
#                             'left': {
#                                 'op': operator.lt,
#                                 'left': Tree(Token('RULE', 'atom'), ['ok']),
#                                 'right': Tree(Token('RULE', 'atom'), [0.0])
#                             },
#                             'right': {
#                                 'op': operator.gt,
#                                 'left': Tree(Token('RULE', 'atom'), ['ok']),
#                                 'right': {
#                                     'op': '-',
#                                     'arg': Tree(Token('RULE', 'atom'), ['our'])  # Undeclared variable
#                                 }
#                             }
#                         },
#                         'block': Tree(Token('RULE', 'block'), [
#                             Tree(Token('RULE', 'statement'), [{
#                                 'type': 'assign',
#                                 'var': 'ok',  # Another attempt to assign to input variable
#                                 'expr': {
#                                     'op': '-',
#                                     'arg': Tree(Token('RULE', 'atom'), ['key'])  # Another undeclared variable
#                                 }
#                             }])
#                         ])
#                     },
#                     {
#                         'type': 'else',
#                         'block': Tree(Token('RULE', 'block'), [
#                             Tree(Token('RULE', 'statement'), [{
#                                 'type': 'assign',
#                                 'var': 'uk',
#                                 'expr': Tree(Token('RULE', 'atom'), [10.0])
#                             }])
#                         ])
#                     }
#                 ]
#             }])
#         ]
#     }])

#     validator = ASTValidator()
    
#     print("Validating AST:")
#     validator.validate(sample_ast)