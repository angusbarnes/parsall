from parsall.core.Streams import CharacterStream

class DefaultLexer:
    def __init__(self, syntax_rules, ignore=" \t\n"):
        self.syntax_rules = syntax_rules
        self.ignore = ignore

    def tokenise(self, input_text):
        # Create a CharacterStream object from the input text
        char_stream = CharacterStream(input_text)

        # Start parsing the tokens using the syntax rules
        parsed_text = []
        while char_stream.peek() is not None:
            while char_stream.peek() in self.ignore:
                char_stream.pop()

            for rule in self.syntax_rules:
                match = rule.match(char_stream)
                if match is not None:
                    parsed_text.append(match)
                    break
            else:
                # If no rule matches, raise an error
                raise ValueError("Syntax error in input text: " + char_stream.peek())

        return parsed_text