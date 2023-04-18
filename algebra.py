from parsall.lexing import DefaultLexer
from textparser import *

rules = [
    AlphaCharacterRule(),
    CharacterSet("Operator", "+'~"),
    CharacterRule("Assignment", "="),
    CharacterSet("Scope", "()")
]

parser = DefaultLexer(rules)

result = parser.parse("ABCZ'+C=(AB)'")
print(result)