from typing import List, Tuple
from core.Streams import TokenStream
from enum import Enum

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



class ASTNode:
    def __init__(self, type_: str, children: List["ASTNode"] = None, value=None):
        self.type = type_
        self.children = children or []
        self.value = value

    def __repr__(self):
        if self.children:
            children_str = ", ".join(repr(c) for c in self.children)
            return f"{self.type}({children_str})"
        elif self.value is not None:
            return f"{self.type}({self.value!r})"
        else:
            return f"{self.type}()"

class ParserRule:
    def __init__(self, parser):
        self.parser = parser

    def match(self):
        raise NotImplementedError()

class NumberRule(ParserRule):
    def match(self):
        if self.parser.peek_token()[0] == "number":
            token = self.parser.get_token()
            return ASTNode("number", value=token[1])
        return None

class ParenRule(ParserRule):
    def match(self):
        if self.parser.peek_token()[0] == "(":
            self.parser.get_token()  # Consume "("
            node = self.parser.parse_expression()
            if self.parser.peek_token()[0] != ")":
                raise ValueError("Missing )")
            self.parser.get_token()  # Consume ")"
            return node
        return None

class UnaryOpRule(ParserRule):
    def __init__(self, parser, op: str):
        super().__init__(parser)
        self.op = op

    def match(self):
        if self.parser.peek_token()[0] == self.op:
            self.parser.get_token()  # Consume operator
            node = self.parser.parse_term()
            return ASTNode(self.op, [node])
        return None

class BinaryOpRule(ParserRule):
    def __init__(self, parser, ops: List[str], next_rule: type):
        super().__init__(parser)
        self.ops = ops
        self.next_rule = next_rule

    def match(self):
        left = self.next_rule().match()

        while self.parser.peek_token()[0] in self.ops:
            op_token = self.parser.get_token()
            right = self.next_rule(self.parser).match()
            left = ASTNode(op_token[1], [left, right])

        return left