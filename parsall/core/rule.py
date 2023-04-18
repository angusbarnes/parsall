from parsall.core.Streams import CharacterStream


class SyntaxRule:
    def match(self, char_stream: CharacterStream) -> str:
        # This method should return a match object if the rule matches
        # the beginning of the token sequence, or None otherwise.
        raise NotImplementedError("SyntaxRule is intended to abstract and as such it cannot be instantiated")