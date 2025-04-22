Tree(
    Token('RULE', 'start'), 
    [
        {'inputs': ['x', 'y'], 'outputs': ['result'], 'variables': {'result', 'x', 'y'}, 
        'statements': [
            Tree(
                Token('RULE', 'statement'), [
                    {'type': 'input_decl', 'vars': ['x', 'y']}
                ]
            ), 
            Tree(
                Token('RULE', 'statement'), [
                    {'type': 'output_decl', 'vars': ['result']}
                ]
            ), 
            Tree(
                Token('RULE', 'statement'), [
                    {'type': 'conditional_block', 'parts': [
                        {'type': 'if', 'condition': {
                            'op': <built-in function and_>, 
                            'left': {
                                'op': <built-in function gt>,
                                'left': Tree(Token('RULE', 'atom'), ['x']),
                                'right': Tree(Token('RULE', 'atom'), [0.0])
                            },
                            'right': {
                                'op': <built-in function gt>,
                                'left': Tree(
                                    Token('RULE', 'atom'), ['y']
                                ), 
                                'right': Tree(
                                    Token('RULE', 'atom'), [0.0]
                                )
                            }
                        }, 
                        'block': Tree(
                            Token('RULE', 'block'), [
                                Tree(Token('RULE', 'statement'), [
                                    {
                                        'type': 'assign', 
                                        'var': 'result', 
                                        'expr': Tree(
                                            Token('RULE', 'atom'), ['x']
                                        )
                                    }
                                ])
                            ]
                        )
                    }, 
                    {'type': 'elif', 'condition': {'op': <built-in function or_>, 'left': {'op': <built-in function lt>, 'left': Tree(Token('RULE', 'atom'), ['x']), 'right': Tree(Token('RULE', 'atom'), [0.0])}, 'right': {'op': <built-in function lt>, 'left': Tree(Token('RULE', 'atom'), ['y']), 'right': Tree(Token('RULE', 'atom'), [0.0])}}, 'block': Tree(Token('RULE', 'block'), [Tree(Token('RULE', 'statement'), [{'type': 'assign', 'var': 'result', 'expr': Tree(Token('RULE', 'atom'), ['x'])}])])}, {'type': 'else', 'block': Tree(Token('RULE', 'block'), [Tree(Token('RULE', 'statement'), [{'type': 'assign', 'var': 'result', 'expr': Tree(Token('RULE', 'atom'), [0.0])}])])}]}])]}])