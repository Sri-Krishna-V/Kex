# Description: Parser for the Kex language
# Detailed workings of the parser: The parser is responsible for parsing the tokens generated by the lexer and constructing an Abstract Syntax Tree (AST) that represents the structure of the program. The parser uses a recursive descent parsing technique to build the AST by following the grammar rules of the Kex language.
# The parser has methods for parsing different types of expressions, statements, and blocks. It uses the lexer to get the next token and checks if the token matches the expected type. If the token matches, it consumes the token and continues parsing. If the token does not match, it raises an error.
# The parser constructs AST nodes for different types of expressions and statements, such as numbers, variables, binary operations, assignments, lists, dictionaries, and conditional statements. It uses these AST nodes to represent the program structure and relationships between different parts of the program.
# The parser also has a method for resetting the current token to the beginning of the input text, allowing the parser to parse multiple input texts without restarting the lexer. This feature is useful for interactive REPL environments where the user can enter multiple expressions or statements to be parsed and interpreted.
# The parser is designed to handle the syntax and grammar rules of the Kex language and ensure that the input text is correctly parsed and transformed into an AST that accurately represents the program structure.

from kex_tokens import TokenType, Token
from kex_ast import AST, BinOp, Num, Var, Assign, ListExpr, DictExpr, String, Boolean


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, expected_type):
        raise Exception(f'Parser error: Expected token type: {expected_type}, got: {self.current_token.type}')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)

    def parse(self):
        return self.assignment()
    # Fix the parse method to return the assignment method

    def assignment(self):
        node = self.variable()
        self.eat(TokenType.ASSIGN)
        node = Assign(left=node, right=self.expr())
        return node

    def variable(self):
        token = self.current_token
        self.eat(TokenType.IDENTIFIER)
        return Var(token)

    def factor(self):
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.FLOAT:
            self.eat(TokenType.FLOAT)
            return Num(token)
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return Num(token)  # You might want to create a String AST node
        elif token.type == TokenType.BOOLEAN:
            self.eat(TokenType.BOOLEAN)
            return Num(token)  # You might want to create a Boolean AST node
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Var(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        self.error(f'Unexpected token: {token.type}')

    def term(self):
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.FLOAT:
            self.eat(TokenType.FLOAT)
            return Num(token)
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token)
        elif token.type == TokenType.BOOLEAN:
            self.eat(TokenType.BOOLEAN)
            return Boolean(token)
        elif token.type == TokenType.IDENTIFIER:
            return self.variable()
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            self.error(f'Unexpected token: {token.type}')

    def expr(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def comparison(self):
        node = self.expr()
        while self.current_token.type in (TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            token = self.current_token
            self.eat(self.current_token.type)
            node = BinOp(left=node, op=token, right=self.expr())
        return node

    def conditional(self):
        self.eat(TokenType.IF)
        condition = self.comparison()
        self.eat(TokenType.COLON)
        if_body = self.block()
        elif_blocks = []
        else_block = None

        while self.current_token.type == TokenType.ELIF:
            self.eat(TokenType.ELIF)
            elif_condition = self.comparison()
            self.eat(TokenType.COLON)
            elif_body = self.block()
            elif_blocks.append((elif_condition, elif_body))

        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.COLON)
            else_block = self.block()

        return {'type': 'IF', 'condition': condition, 'if_body': if_body, 'elif_blocks': elif_blocks, 'else_block': else_block}

    def block(self):
        # Assuming block is a multi statement or a list of statements for complexity
        self.eat(TokenType.LBRACE)
        statements = []
        while self.current_token.type != TokenType.RBRACE:
            statements.extend(self.statement())
        self.eat(TokenType.RBRACE)
        return statements

    def statement(self):
        if self.current_token.type == TokenType.IF:
            return self.conditional()
        # Add more statement types here (assignments, loops, etc.)
        elif self.current_token.type == TokenType.IDENTIFIER:
            left = self.current_token
            self.eat(TokenType.IDENTIFIER)
            op = self.current_token
            if op.type == TokenType.ASSIGN:
                self.eat(TokenType.ASSIGN)
                right = self.expr()
                return Assign(left, op, right)
            else:
                self.error(f'Unexpected token: {op.type}')
        else:
            self.error(f'Unexpected token: {self.current_token.type}')

        return self.expr()

    def reset(self):
        self.current_token = self.lexer.get_next_token()
