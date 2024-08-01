# Description: This file contains the lexer class for the Kex language. 
# Detailed working of kex_lexer class: The lexer is responsible for tokenizing the input text and converting it into a sequence of tokens that represent the different parts of the program. The lexer reads the input text character by character and generates tokens based on the rules of the Kex language.
# The lexer has methods for getting the next token, skipping whitespace, and parsing different types of tokens such as numbers, strings, identifiers, and keywords. It uses regular expressions to match the input text with the token patterns and generates tokens with the appropriate type and value.
# The lexer also keeps track of the current position in the input text, line number, and column number to provide meaningful error messages in case of syntax errors. It raises an exception if it encounters an invalid character or token in the input text.
# The lexer is designed to work in conjunction with the parser to tokenize the input text and provide the tokens needed to build the Abstract Syntax Tree (AST) that represents the program structure. It ensures that the input text is correctly tokenized and ready for parsing and interpretation by the parser.
# The lexer is an essential component of the Kex interpreter as it converts the raw input text into a format that can be processed by the parser and interpreter to execute the program logic.



from kex_tokens import Token, TokenType
from kex_ast import AST, BinOp, Num, Var, Assign, ListExpr, DictExpr

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.line = 1
        self.column = 1

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(
            self.text) else None

    def number(self):
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return Token(TokenType.INTEGER, int(result), self.line, self.column)

    def string(self):
        result = ''
        self.advance()  # Skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # Skip the closing quote
        return Token(TokenType.STRING, result, self.line, self.column)

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def identifier_or_keyword(self):
        result = ''
        start_pos = self.pos
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        if result == 'if':
            return Token(TokenType.IF, result, self.line, start_pos)
        elif result == 'elif':
            return Token(TokenType.ELIF, result, self.line, start_pos)
        elif result == 'else':
            return Token(TokenType.ELSE, result, self.line, start_pos)
        elif result == 'true':
            return Token(TokenType.BOOLEAN, True, self.line, start_pos)
        elif result == 'false':
            return Token(TokenType.BOOLEAN, False, self.line, start_pos)
        return Token(TokenType.IDENTIFIER, result, self.line, start_pos)
    

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier_or_keyword()

            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()

            if self.current_char == '"':
                return self.string()

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQ, '==', self.line, self.column - 1)
                return Token(TokenType.ASSIGN, '=', self.line, self.column - 1)

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.NE, '!=', self.line, self.column - 1)
                else:
                    raise Exception(f'Invalid character: ! at line {self.line}, column {self.column}')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LE, '<=', self.line, self.column - 1)
                return Token(TokenType.LT, '<', self.line, self.column - 1)

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GE, '>=', self.line, self.column - 1)
                return Token(TokenType.GT, '>', self.line, self.column - 1)

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+', self.line, self.column - 1)
            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-', self.line, self.column - 1)
            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MUL, '*', self.line, self.column - 1)
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIV, '/', self.line, self.column - 1)
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', self.line, self.column - 1)
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', self.line, self.column - 1)
            if self.current_char == '[':
                self.advance()
                return Token(TokenType.LBRACKET, '[', self.line, self.column - 1)
            if self.current_char == ']':
                self.advance()
                return Token(TokenType.RBRACKET, ']', self.line, self.column - 1)
            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE, '{', self.line, self.column - 1)
            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE, '}', self.line, self.column - 1)
            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',', self.line, self.column - 1)
            if self.current_char == ':':
                self.advance()
                return Token(TokenType.COLON, ':', self.line, self.column - 1)
            # If we get here, we have an invalid character
            raise Exception(f'Invalid character: {self.current_char} at line {self.line}, column {self.column}')

        return Token(TokenType.EOF, None, self.line, self.column)

    def reset(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.line = 1
        self.column = 1

    
