# Description: Token types and Token class for the Kex language.
# Detailed working of Kex_token class: The Token class represents a token in the Kex language, which consists of a type, value, line number, and column number. The TokenType enum defines the different types of tokens that can be generated by the lexer, such as integers, floats, strings, booleans, identifiers, and special symbols like parentheses, brackets, and operators.
# The Token class has attributes for the token type, value, line number, and column number, which are used to store the information about the token generated by the lexer. The __repr__ method is implemented to provide a string representation of the token for debugging and logging purposes.


import re
from enum import Enum, auto

class TokenType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    IDENTIFIER = auto()

    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    COLON = auto()
    EOF = auto()

    IF = auto()
    ELIF = auto()
    ELSE = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()


class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)}, line={self.line}, col={self.column})'
