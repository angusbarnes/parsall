from parsall.lexing import DefaultLexer
from textparser import *

rules = [
    AlphaCharacterRule(),
    CompoundRule("Comment", [
        (CharacterRule("", '#'), False),
        (
            GreedyConsumerRule(
                Ruleset([IdentifierRule(), CharacterRule("", ' ')]),
                CharacterRule("",'\n')
            ),
            True
        )
    ]),
    CharacterSet("Operator", "+'~"),
    CharacterRule("Assignment", "="),
    CharacterSet("Scope", "()")
]

parser = DefaultLexer(rules)

result = parser.parse("#test hm\nABCZ'+C=(AB)'")
print(result)