from parsall.lexing import DefaultLexer
from parsall.core.Streams import TokenStream
from parsall.core.rule import *

rules = [
    AlphaCharacterRule(),
    CommentRule("#", '\n'),
    CharacterSet("Operator", "+'~"),
    CharacterRule("Assignment", "="),
    CharacterSet("Scope", "()")
]

lexer = DefaultLexer(rules)

result = lexer.tokenise("ABCZ'+C'(AB)'")

is_symbol = lambda x: x[0] == 'Symbol'

tokens = TokenStream(result)

def collect_symbol(tokens: TokenStream):
    _, symbol = tokens.pop()
    
    if tokens.peek()[1] == "'":
        tokens.pop()
        return ('NOT', symbol)
    else:
        return (symbol)
    
def collect_term(tokens: TokenStream):
    ANDS = []
    while is_symbol(tokens.peek()):
        ANDS.append(collect_symbol(tokens))
    else:
        return ('AND', ANDS)
    
def collect_expression(tokens: TokenStream):

    expr = ""

    if tokens.peek()[1] == '(':
        tokens.pop()
        expr = collect_expression(tokens)
        if tokens.pop()[1] != ')':
            raise SyntaxError("Unbalanced brackets found in expression")
    else:
        expr = collect_term(tokens)

    if tokens.peek()[1] == "+":
        tokens.pop()
        return ('OR', expr, collect_expression(tokens))
    elif tokens.peek()[1] == '(':
        ANDS = [expr]
        ANDS.append(collect_expression(tokens))
        return ('AND', ANDS)
    elif tokens.peek()[1] == "'":
        return ('NOT', expr)
    else:
        return (expr)

tree = []
tree = collect_expression(tokens)


from pprint import pprint
pprint(tree)