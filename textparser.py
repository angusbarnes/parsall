from typing import List, Tuple
from parsall.core.Streams import CharacterStream
from parsall.lexing import DefaultLexer
from parsall.core.rule import *
from parsall.semantics import python

if __name__ == "__main__":

    rules = [
        WordSet("keyword", python.keywords), 
        IdentifierRule(), 
        NumberRule(), 
        CharacterSet("operator", python.standard_operators), 
        CharacterSet("bracket", python.standard_brackets), 
        CharacterSet("delim", ',.:'), 
        CharacterRule("newline", '\n'), 
        CommentRule("#", '\n'),
        StringRule()
    ]

    lexer = DefaultLexer(rules, ignore=" ;\t\r")

    text = ""
    with open("test.code", 'r') as file:
        text = file.read()

    import pprint
    result = lexer.tokenise(text)

    with open("lexer.log", "w") as log_file:
        pprint.pprint(result, log_file)

    count = 0
    assignment_count = 0
    for i in range(len(result)-3):
        tok1 = result[i]
        tok2 = result[i+1]
        tok3 = result[i+2]

        if tok1[0] == "keyword" and tok2[0] == "symbol" and tok3[0] == "bracket":
            if tok1[1] == 'def':
                count += 1
        elif tok1[1] == '=':
            assignment_count += 1

    print(f"{count} total functions were found and {assignment_count} variable assignments were made")