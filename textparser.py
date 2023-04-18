from parsall.core.Streams import CharacterStream
from parsall.lexing import DefaultLexer
from parsall.core.rule import SyntaxRule
from parsall.semantics import python
import parsall.semantics.syntax as syntax


#TODO: ignore case is currently not implemented
class WordRule(SyntaxRule):
    def __init__(self, token_name, word, *, ignore_case = False):
        self.word = word
        self.token_name = token_name
        self.length = len(word)

    def match(self, char_stream: CharacterStream) -> str:

        # Check if the next characters in the stream match the target word
        if char_stream.lookahead(self.length) != self.word:
            return None
        
        if char_stream.peek(self.length).isalpha():
            return None

        # If the target word is present, consume the same number of characters as the length of the word
        match_text = ""
        for _ in range(len(self.word)):
            match_text += char_stream.pop()

        # Return the word as a match object
        return (self.token_name, match_text)

class NumberRule(SyntaxRule):
    def match(self, char_stream: CharacterStream) -> str:
        # Attempt to consume characters until a non-digit character is encountered
        match_text = ""
        while char_stream.peek() is not None and char_stream.peek().isdigit():
            match_text += char_stream.pop()

        # If we successfully consume at least one digit, return the number as a match object
        if match_text:
            return ("Number", int(match_text))
        else:
            return None
        
class IdentifierRule(SyntaxRule):
    def match(self, char_stream: CharacterStream) -> str:
        # Check if the first character is a letter or underscore
        first_char = char_stream.peek()
        if not first_char.isalpha() and first_char != '_':
            return None
        
        # Check that the identifier does not start with a number
        if first_char.isdigit():
            return None
        
        # Start building the identifier
        identifier = char_stream.pop()
        
        # Add any additional letters, underscores, or digits
        while True:
            next_char = char_stream.peek()
            if next_char is None or not (next_char.isalnum() or next_char == '_'):
                break
            identifier += char_stream.pop()
        
        return ("symbol", identifier)
    
class StringRule(SyntaxRule):
    def match(self, char_stream: CharacterStream) -> str:
        quote = char_stream.peek()
        if quote != '"' and quote != "'":
            return None

        # Consume the opening quote
        char_stream.pop()

        match_text = ""
        while True:
            next_char = char_stream.pop()
            if next_char == quote:
                return ("string", match_text)
            elif next_char == "\\":
                # Consume the escaped character
                next_char = char_stream.pop()
                if next_char is None:
                    raise ValueError("Syntax error in input text")
                elif next_char == quote or next_char in "\\trxn":
                    match_text += next_char
                else:
                    raise ValueError("Syntax error in input text: " + next_char)
            else:
                match_text += next_char

            if char_stream.peek() is None:
                raise ValueError("Syntax error in input text")
            
class CharacterRule(SyntaxRule):
    def __init__(self, token_name, character):
        self.character = character
        self.token_name = token_name

    def match(self, char_stream: CharacterStream) -> str:
        if char_stream.peek() == self.character:
            return (self.token_name, char_stream.pop())
        else:
            return None

class CompoundRule(SyntaxRule):
    def __init__(self, token_name, rules_config):
        self.rules = rules_config
        self.token_name = token_name

    def match(self, text):
        match_text = ""
        for rule, include_text in self.rules:
            rule_match = rule.match(text)
            if rule_match is None:
                return None
            if include_text:
                match_text += rule_match
            text = text[len(rule_match):]
        return (self.token_name, match_text)


class Ruleset(SyntaxRule):
    def __init__(self, rules):
        self.rules = rules

    def match(self, text):
        for rule in self.rules:
            match = rule.match(text)
            if match:
                return match
        return None
    
class CharacterSet(Ruleset):
    def __init__(self, token_name, characters):
        self.rules = []
        for c in characters:
            self.rules.append(CharacterRule(token_name, c))

class WordSet(Ruleset):
    def __init__(self, token_name, words: list[str]):
        self.rules = []
        for word in words:
            self.rules.append(WordRule(token_name, word))

class AlphaCharacterRule(SyntaxRule):
    def match(self, char_stream: CharacterStream):

        code = ord(char_stream.peek())
        if ord('A') <= code <= ord('Z'):
            return ("Symbol", char_stream.pop())
        
        return None
    
class GreedyConsumerRule(SyntaxRule):
    pass

    
#operator_rule = Ruleset([CharacterRule("+"), CharacterRule("-"), CharacterRule("/")])

if __name__ == "__main__":

    rules = [
        WordSet("keyword", python.keywords), 
        IdentifierRule(), 
        NumberRule(), 
        CharacterSet("operator", python.standard_operators), 
        CharacterSet("bracket", python.standard_brackets), 
        CharacterSet("delim", '#,.:'), 
        CharacterRule("newline", '\n'), 
        StringRule()
    ]

    parser = DefaultLexer(rules, ignore=" ;\t\r")

    text = ""
    with open("test.code", 'r') as file:
        text = file.read()

    from pprint import pprint
    result = parser.parse(text)

    count =0
    decorator = None
    for i in range(len(result)-3):
        tok1 = result[i]
        tok2 = result[i+1]
        tok3 = result[i+2]

        if tok1[1] == '@':
            decorator = tok2[1]

        if tok1[0] == "keyword" and tok2[0] == "symbol" and tok3[0] == "bracket":
            if tok1[1] == 'def':
                print(f"Function definition with name: {tok2[1]} decorated with: {decorator}")
                count += 1
                decorator = None

    print(f"{count} total functions were found")