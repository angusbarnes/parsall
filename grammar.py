from enum import Enum


class Expression:
    def __init__(self, one, two):
        pass

class Identifier:
    pass

class RuleGroup:
    pass

class Assigment:
    pass

class UnaryOP:
    pass

class KeyWordStatement:
    pass

class Chain:
    pass

class MatchTokenID:
    pass

class MatchToken:
    pass

class Ignore:
    pass

class TokenType(Enum):
    Identifier = 1
    Keyword = 2
    Operator = 3
    Delimiter = 4
    Literal = 5
    Comment = 6
    String = 7
    Regular_Expression = 8
    Markup_Tag = 9
    Entity_Reference = 10
    Whitespace = 11
    Directive = 12
    Number = 13
    Float = 14
    Int = 15
    Word = 16
    Grammar = 17
    ScopeModifier = 18
    Bracket = 19

symbol = MatchTokenID(TokenType.Identifier)
def_keyword = MatchToken(TokenType.Keyword, "def")

function_def = Chain([def_keyword, symbol])

# will match function defs, will ignore all else
grammar = [
    function_def,
    Ignore()
]

parser = Parser(grammar)
parser.parse(tokens)