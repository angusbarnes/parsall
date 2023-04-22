from parsall.lexing import DefaultLexer
from textparser import *

rules = [
    AlphaCharacterRule(),
    CommentRule("#", '\n'),
    CharacterSet("Operator", "+'~"),
    CharacterRule("Assignment", "="),
    CharacterSet("Scope", "()")
]

parser = DefaultLexer(rules)

result = parser.parse("#test hm\nABCZ'+C=(AB)'")
print(result)