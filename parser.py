from lark import Lark, Transformer, v_args
import operator

grammar = r"""
start: program
program: statement*

statement: input_stmt
         | output_stmt
         | assign_stmt
         | conditional_block
         
conditional_block: if_stmt [elif_block*] [else_clause]

input_stmt: "INPUT" ident_list
output_stmt: "OUTPUT" ident_list
assign_stmt: "assign" IDENT "=" expr

if_stmt: "IF" condition "THEN" block
elif_block: "ELIF" condition "THEN" block
else_clause: "ELSE" block

block: statement+

condition: expr comp_op expr
        | condition logic_op condition  -> logic_cond
        | "NOT" condition -> not_cond
        | "(" condition ")" -> paren_cond

comp_op: "==" -> eq
       | ">=" -> ge
       | "<" -> lt
       | ">" -> gt
       | "<=" -> le
       | "!=" -> ne

logic_op: "AND" -> and_op
        | "OR" -> or_op

expr: term ( ("+" | "-") term )*
term: factor ( ("*" | "/") factor )*
factor: power ( "%" power )? -> mod_op
power: atom ( "^" atom )? -> pow_op
atom: NUMBER | IDENT | "-" atom -> neg_atom | "(" expr ")" -> paren_expr
ident_list: IDENT ("," IDENT)*

IDENT: /[a-zA-Z][a-zA-Z0-9_]*/
NUMBER: /[0-9]+(\.[0-9]+)?/
COMMENT: /\/\/[^\n]*/
      | /\/\*([^*]|\*[^\/])*\*\//

%ignore /[ \t\f\r\n]+/
%ignore COMMENT
"""

class PseudocodeTransformer(Transformer):
    def __init__(self):
        self.variables = {}
        self.outputs = []
        self.inputs = []

    @v_args(inline=True)
    def NUMBER(self, value):
        return float(value)

    @v_args(inline=True)
    def IDENT(self, value):
        return str(value)

    @v_args(inline=True)
    def atom(self, value):
        if isinstance(value, str):
            if value not in self.variables:
                raise ValueError(f"Undefined variable: {value}")
            return self.variables[value]
        return value

    def neg_atom(self, children):
        return -children[0]

    def paren_expr(self, children):
        return children[0]

    def mod_op(self, children):
        if len(children) == 1:
            return children[0]
        return operator.mod(children[0], children[1])

    def pow_op(self, children):
        if len(children) == 1:
            return children[0]
        return operator.pow(children[0], children[1])

    def term(self, children):
        result = children[0]
        for op, value in zip(children[1::2], children[2::2]):
            if op == '*':
                result *= value
            elif op == '/':
                result /= value
        return result

    def expr(self, children):
        result = children[0]
        for op, value in zip(children[1::2], children[2::2]):
            if op == '+':
                result += value
            elif op == '-':
                result -= value
        return result

    # Operator methods
    def eq(self, _):
        return operator.eq
    
    def ge(self, _):
        return operator.ge
    
    def lt(self, _):
        return operator.lt
    
    def gt(self, _):
        return operator.gt
    
    def le(self, _):
        return operator.le
    
    def ne(self, _):
        return operator.ne
    
    def and_op(self, _):
        return operator.and_
    
    def or_op(self, _):
        return operator.or_
    
    def logic_cond(self, children):
        left, op, right = children
        return op(bool(left), bool(right))
    
    def not_cond(self, children):
        return not bool(children[0])
    
    def paren_cond(self, children):
        return children[0]

    def ident_list(self, children):
        return children

    def input_stmt(self, children):
        for var in children[0]:
            self.inputs.append(var)
            self.variables[var] = float(input(f"Enter value for {var}: "))
        return None

    def output_stmt(self, children):
        for var in children[0]:
            if var not in self.variables:
                raise ValueError(f"Undefined output variable: {var}")
            self.outputs.append((var, self.variables[var]))
        return None

    def assign_stmt(self, children):
        var, value = children
        self.variables[var] = value
        return None

    def condition(self, children):
        left, op, right = children
        return op(left, right)

    def if_stmt(self, children):
        condition_result, block = children
        return ("if", condition_result, block)

    def elif_block(self, children):
        condition_result, block = children
        return ("elif", condition_result, block)

    def else_clause(self, children):
        return ("else", True, children[0])

    def conditional_block(self, children):
        executed = False
        
        # Process if statement
        if_type, if_condition, if_block = children[0]
        if if_condition:
            executed = True
            for stmt in if_block:
                if stmt is not None:
                    self._call_user(stmt)
        
        # Process elif blocks (if any)
        i = 1
        while i < len(children) and children[i][0] == "elif" and not executed:
            _, elif_condition, elif_block = children[i]
            if elif_condition:
                executed = True
                for stmt in elif_block:
                    if stmt is not None:
                        self._call_user(stmt)
            i += 1
        
        # Process else clause (if present and no other block executed)
        if i < len(children) and children[i][0] == "else" and not executed:
            _, _, else_block = children[i]
            for stmt in else_block:
                if stmt is not None:
                    self._call_user(stmt)
        
        return None

    def block(self, children):
        return children

    def program(self, children):
        for stmt in children:
            if stmt is not None:
                self._call_user(stmt)
        return self.outputs

    def _call_user(self, stmt):
        if isinstance(stmt, tuple):
            if len(stmt) == 3 and stmt[0] in ("if", "elif", "else"):
                # This should not happen as conditional blocks are processed in conditional_block
                pass
            else:
                cond, stmts = stmt
                if cond:
                    for s in stmts:
                        self._call_user(s)
        elif isinstance(stmt, list):
            for s in stmt:
                self._call_user(s)

def execute_pseudocode(code):
    try:
        parser = Lark(grammar, parser='lalr')
        tree = parser.parse(code)
        transformer = PseudocodeTransformer()
        outputs = transformer.transform(tree)
        return {
            'variables': transformer.variables,
            'inputs': transformer.inputs,
            'outputs': outputs
        }
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    pseudocode = """
    // This is a simple test program with nested if statements, 
    /* This is a multi-line comment
       to demonstrate comment support */
    
    INPUT x, y
    OUTPUT x, y
    
    // Testing nested if statements
    IF x > 0 THEN
        assign x = x + 10
        
        // Nested if statement
        IF y > 0 THEN
            assign y = y * 2
        ELSE
            assign y = y - 5
        
        // Testing new operators
        assign z = (x % 3) ^ 2  // modulo and power
    ELIF x < 0 THEN
        assign x = x - 10
        
        // Logical operators
        IF y < 0 AND x < -15 THEN
            assign y = y * -1 + 15 / 20
        ELIF NOT (y == 0) OR x == -10 THEN
            assign y = y + 7
        ELSE
            assign y = 0
    ELSE
        assign x = 0
        assign y = 0
    """

    result = execute_pseudocode(pseudocode)
    print("\nExecution results:")
    print(f"Variables: {result.get('variables', {})}")
    print(f"Outputs: {result.get('outputs', [])}")
    if 'error' in result:
        print(f"Error: {result['error']}")