from typing import List, Tuple


class Stream:
    """A generic stream that can be iterated over and provides methods to pop the next item or peek at it without popping it."""

    def __init__(self, items, length):
        """
        Initialize a new stream.

        Args:
            items: The sequence of items to use as the stream.
        """
        self.items = items
        self.position = 0
        self.length = length

    def pop(self):
        """
        Pop the next item from the stream and return it.

        Raises:
            IndexError: If the end of the stream has been reached.

        Returns:
            The next item in the stream.
        """
        if self.position >= self.length:
            raise IndexError()

        item = self.items[self.position]
        self.position += 1
        return item

    def peek(self, n=0):
        """
        Return the next item in the stream without popping it.

        Returns:
            The next item in the stream, or None if the end of the stream has been reached.
        """
        if self.position + n >= self.length:
            return None

        return self.items[self.position+n]

    def lookahead(self, n) -> str:
        """
        Returns the next `n` items in the input stream without consuming them.
        """
        return self.items[self.position : self.position + n]

    def __iter__(self):
        """
        Return an iterator over the stream.

        Returns:
            An iterator over the stream.
        """
        return self

    def __next__(self):
        """
        Pop the next item from the stream and return it.

        Raises:
            StopIteration: If the end of the stream has been reached.

        Returns:
            The next item in the stream.
        """
        if self.position < self.length:
            return self.pop()

        raise StopIteration()
    
class TokenStream(Stream):
    def __init__(self, tokens: List[Tuple]):
        super().__init__(tokens, len(tokens))

class CharacterStream(Stream):
    """A character stream that can be iterated over and provides methods to pop the next character or peek at it without popping it."""

    def __init__(self, stream: str):
        """
        Initialize a new character stream.

        Args:
            stream (str): The string to use as the character stream.
        """
        super().__init__(stream, len(stream))