from typing import List, Tuple
from parsall.core.Streams import CharacterStream

class SyntaxRule:
    """ 
        Abstract Class
        ------
        The base class for lexer rules. Inherit from this class to define a custom rule.
        The rule should at least impliment the `match(self, char_stream: CharacterStream)`
        function - this is used for the lexing stage.
    """

    def match(self, char_stream: CharacterStream) -> str:
        """
            Implement your match condition here.

            Returns
            -------
                None if a match is not found, otherwise return the token created
        """
        # This method should return a match object if the rule matches
        # the beginning of the token sequence, or None otherwise.
        raise NotImplementedError("SyntaxRule is intended to abstract and as such it cannot be instantiated")#TODO: ignore case is currently not implemented

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
    def __init__(self, token_name, rules_config: List[Tuple[SyntaxRule, bool]]):
        self.rules = rules_config
        self.token_name = token_name

    def match(self, text):
        match_text = ""
        for rule, include_text in self.rules:
            rule_match = rule.match(text)
            if rule_match is None:
                return None
            if include_text:
                match_text += rule_match[1]
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

class CommentRule(SyntaxRule):
    def __init__(self, comment_pattern, terminator) -> None:
        self.begin = comment_pattern
        self.terminator = terminator
        self.pattern_length = len(comment_pattern)
    def match(self, char_stream: CharacterStream) -> str:
        
        if char_stream.lookahead(self.pattern_length) != self.begin:
            return None
        
        char_stream.advance(self.pattern_length)

        comment_string = ""
        while char_stream.peek() != self.terminator:
            comment_string += char_stream.pop()

        # TODO: Provide a global method to eat a terminating chacter and raise
        #       required errors
        result = CharacterRule("", self.terminator).match(char_stream)

        if not result:
            raise SyntaxError(char_stream.peek())
        
        return ("Comment", comment_string)


class AlphaCharacterRule(SyntaxRule):
    def match(self, char_stream: CharacterStream):

        code = ord(char_stream.peek())
        if ord('A') <= code <= ord('Z'):
            return ("Symbol", char_stream.pop())
        
        return None
    
class GreedyConsumerRule(SyntaxRule):
    def __init__(self, consume_rule: SyntaxRule, end_rule: SyntaxRule):
        self.consumer = consume_rule
        self.end = end_rule

    def match(self, char_stream: CharacterStream):

        value = ""
        while token := self.consumer.match(char_stream):
            value += token[1]

        result = self.end.match(char_stream)

        if not result:
            raise SyntaxError(char_stream.peek())
        
        return ("", value)
    

