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

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)}, line={self.line}, col={self.column})'

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
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        if self.current_char == '/':
            self.advance()
            if self.current_char == '/':
                # Single-line comment
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                self.advance()
            elif self.current_char == '*':
                # Multi-line comment
                self.advance()
                while self.current_char is not None:
                    if self.current_char == '*' and self.peek() == '/':
                        self.advance()
                        self.advance()
                        break
                    self.advance()
            else:
                return Token(TokenType.DIV, '/', self.line, self.column - 1)
        return None

    def peek(self):
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    def number(self):
        result = ''
        start_pos = self.pos
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        if '.' in result:
            return Token(TokenType.FLOAT, float(result), self.line, start_pos)
        else:
            return Token(TokenType.INTEGER, int(result), self.line, start_pos)

    def string(self):
        result = ''
        start_pos = self.pos
        self.advance()  # skips the opening quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char is None:
            raise Exception(f'Unterminated string at line {self.line}, column {start_pos}')
        self.advance()  # skips the closing quote
        return Token(TokenType.STRING, result, self.line, start_pos)

    def identifier(self):
        result = ''
        start_pos = self.pos
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        if result == 'true':
            return Token(TokenType.BOOLEAN, True, self.line, start_pos)
        elif result == 'false':
            return Token(TokenType.BOOLEAN, False, self.line, start_pos)
        return Token(TokenType.IDENTIFIER, result, self.line, start_pos)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char == '/':
                comment_token = self.skip_comment()
                if comment_token:
                    return comment_token
                continue
            
            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()
            
            if self.current_char == '"':
                return self.string()
            
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            
            # Single-character tokens
            for token_type, char in [
                (TokenType.ASSIGN, '='),
                (TokenType.PLUS, '+'),
                (TokenType.MINUS, '-'),
                (TokenType.MUL, '*'),
                (TokenType.LPAREN, '('),
                (TokenType.RPAREN, ')'),
                (TokenType.LBRACKET, '['),
                (TokenType.RBRACKET, ']'),
                (TokenType.LBRACE, '{'),
                (TokenType.RBRACE, '}'),
                (TokenType.COMMA, ','),
                (TokenType.COLON, ':'),
            ]:
                if self.current_char == char:
                    token = Token(token_type, char, self.line, self.column)
                    self.advance()
                    return token
            
            # If we get here, we have an invalid character
            raise Exception(f'Invalid character: {self.current_char} at line {self.line}, column {self.column}')
        
        return Token(TokenType.EOF, None, self.line, self.column)

    def debug_tokens(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        print("DEBUG: Tokens:", tokens)
        return tokens

class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
    
    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    
    def __repr__(self):
        return f"Num({self.value})"

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    
    def __repr__(self):
        return f"Var({self.value})"

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class ListExpr(AST):
    def __init__(self, elements):
        self.elements = elements

class DictExpr(AST):
    def __init__(self, pairs):
        self.pairs = pairs

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        print(f"DEBUG: Factor token: {token}")
        if token.type in (TokenType.INTEGER, TokenType.FLOAT, TokenType.STRING, TokenType.BOOLEAN):
            self.eat(token.type)
            return Num(token)
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Var(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        elif token.type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET)
            elements = []
            while self.current_token.type != TokenType.RBRACKET:
                elements.append(self.expr())
                if self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
            self.eat(TokenType.RBRACKET)
            return ListExpr(elements)
        elif token.type == TokenType.LBRACE:
            self.eat(TokenType.LBRACE)
            pairs = {}
            while self.current_token.type != TokenType.RBRACE:
                key = self.expr()
                self.eat(TokenType.COLON)
                value = self.expr()
                pairs[key.value] = value
                if self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
            self.eat(TokenType.RBRACE)
            return DictExpr(pairs)

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            print(f"DEBUG: Term token: {token}")
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.DIV):
            token = self.current_token
            print(f"DEBUG: Term token: {token}")
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def assignment(self):
        left = self.expr()
        if isinstance(left, Var) and self.current_token.type == TokenType.ASSIGN:
            token = self.current_token
            self.eat(TokenType.ASSIGN)
            right = self.expr()
            return Assign(left, token, right)
        return left

    def parse(self):
        return self.assignment()

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def get(self, name):
        return self.symbols.get(name)

    def set(self, name, value):
        self.symbols[name] = value

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.symbol_table = SymbolTable()

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        print(f"DEBUG: Left: {left}, Right: {right}, Op: {node.op.type}")  # Debug print
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if node.op.type == TokenType.PLUS:
                return left + right
            elif node.op.type == TokenType.MINUS:
                return left - right
            elif node.op.type == TokenType.MUL:
                return left * right
            elif node.op.type == TokenType.DIV:
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                return left / right
        elif isinstance(left, str) and isinstance(right, str) and node.op.type == TokenType.PLUS:
            return left + right
        else:
            raise TypeError(f"Unsupported operand types for {node.op.value}: '{type(left).__name__}' and '{type(right).__name__}'")
            
    def visit_Num(self, node):
        return node.value

    def visit_Var(self, node):
        value = self.symbol_table.get(node.value)
        if value is None:
            raise NameError(f"Name '{node.value}' is not defined")
        return value

    def visit_Assign(self, node):
        var_name = node.left.value
        value = self.visit(node.right)
        self.symbol_table.set(var_name, value)
        return value

    def visit_ListExpr(self, node):
        return [self.visit(element) for element in node.elements]

    def visit_DictExpr(self, node):
        return {key: self.visit(value) for key, value in node.pairs.items()}

    def interpret(self):
        tree = self.parser.parse()
        print(f"DEBUG: Term token: {self.parser.current_token}")
        return self.visit(tree)
 

def main():
    lexer = Lexer('')
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    while True:
        try:
            text = input('kex>> ')
            if text.strip() == '':
                continue
            if text.strip().lower() == 'exit':
                break
            lexer.text = text
            lexer.pos = 0
            lexer.current_char = lexer.text[lexer.pos] if lexer.text else None
            parser.current_token = lexer.get_next_token()
            result = interpreter.interpret()
            if result is not None:
                print(result)
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == '__main__':
    print("Welcome to Kex! Type 'exit' to quit.")
    main()
    print("Goodbye!")

