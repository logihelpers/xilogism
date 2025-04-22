from lark import Lark, Transformer, v_args
import operator

grammar = r"""
start: program
program: statement*

statement: input_decl
         | output_decl
         | assign_stmt
         | conditional_block
         
conditional_block: if_stmt [elif_block*] [else_clause]

input_decl: "INPUT" ident_list
output_decl: "OUTPUT" ident_list
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
factor: atom ( "%" atom )? -> mod_op
atom: NUMBER | IDENT | "-" atom -> neg_atom | "(" expr ")" -> paren_expr
ident_list: IDENT ("," IDENT)*

IDENT: /[a-zA-Z][a-zA-Z0-9_]*/
NUMBER: /[0-9]+(\.[0-9]+)?/
COMMENT: /\/\/[^\n]*/
      | /\/\*([^*]|\*[^\/])*\*\//

%ignore /[ \t\f\r\n]+/
%ignore COMMENT
"""

class PseudocodeParser(Transformer):
    def __init__(self):
        self.ast = {
            'inputs': [],
            'outputs': [],
            'variables': set(),
            'statements': []
        }

    @v_args(inline=True)
    def NUMBER(self, token):
        return float(token.value)

    @v_args(inline=True)
    def IDENT(self, token):
        self.ast['variables'].add(token.value)
        return token.value

    def ident_list(self, children):
        return children

    def input_decl(self, children):
        vars_list = children[0]
        self.ast['inputs'].extend(vars_list)
        return {'type': 'input_decl', 'vars': vars_list}

    def output_decl(self, children):
        vars_list = children[0]
        self.ast['outputs'].extend(vars_list)
        return {'type': 'output_decl', 'vars': vars_list}

    def assign_stmt(self, children):
        var, expr = children
        return {'type': 'assign', 'var': var, 'expr': expr}

    def if_stmt(self, children):
        cond, block = children
        return {'type': 'if', 'condition': cond, 'block': block}

    def elif_block(self, children):
        cond, block = children
        return {'type': 'elif', 'condition': cond, 'block': block}

    def else_clause(self, children):
        return {'type': 'else', 'block': children[0]}

    def conditional_block(self, children):
        return {'type': 'conditional_block', 'parts': children}

    def program(self, children):
        self.ast['statements'] = children
        return self.ast

    # Operator methods
    def eq(self, _=None): return operator.eq
    def ge(self, _=None): return operator.ge
    def lt(self, _=None): return operator.lt
    def gt(self, _=None): return operator.gt
    def le(self, _=None): return operator.le
    def ne(self, _=None): return operator.ne
    def and_op(self, _=None): return operator.and_
    def or_op(self, _=None): return operator.or_

    # Expression handlers
    def neg_atom(self, children): return {'op': '-', 'arg': children[0]}
    def paren_expr(self, children): return children[0]
    def mod_op(self, children):
        if len(children) == 1: return children[0]
        return {'op': '%', 'left': children[0], 'right': children[1]}
    
    def term(self, children):
        if len(children) == 1:
            return children[0]
        result = children[0]
        for i in range(1, len(children), 2):
            if i+1 >= len(children):
                break
            result = {'op': children[i], 'left': result, 'right': children[i+1]}
        return result
        
    def expr(self, children):
        if len(children) == 1:
            return children[0]
        result = children[0]
        for i in range(1, len(children), 2):
            if i+1 >= len(children):
                break
            result = {'op': children[i], 'left': result, 'right': children[i+1]}
        return result
        
    # Condition handlers
    def logic_cond(self, children): 
        left, op, right = children
        return {'op': op, 'left': left, 'right': right}
    def not_cond(self, children): return {'op': 'NOT', 'arg': children[0]}
    def paren_cond(self, children): return children[0]
    def condition(self, children): 
        if len(children) == 3:
            left, op, right = children
            return {'op': op, 'left': left, 'right': right}
        return children[0]

# def parse_pseudocode(code):
#     parser = Lark(grammar, parser='lalr')
#     transformer = PseudocodeParser()
#     tree = parser.parse(code)
#     return transformer.transform(tree)

# if __name__ == "__main__":
#     test_code = """
#     INPUT x, y
#     OUTPUT result
    
#     IF x > 0 AND y > 0 THEN
#         assign result = (x + y) * 2
#     ELIF x < 0 OR y < 0 THEN
#         assign result = (x - y) / 2
#     ELSE
#         assign result = 0
#     """
    
#     ast = parse_pseudocode(test_code)
#     print("Parsed AST Structure:")
#     import pprint
#     pprint.pprint(ast, indent=4)