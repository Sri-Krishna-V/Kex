from kex_Nodevisitor import NodeVisitor
from kex_symbolTable import SymbolTable
from kex_ast import BinOp, Num, Var, Assign, ListExpr, DictExpr
from kex_tokens import TokenType


class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.symbol_table = SymbolTable()  # Initialize a symbol table

    def visit_VAR(self, node):
        # Retrieve the value from the symbol table
        return self.symbol_table.get(node['value'])

    def visit_Assign(self, node):
        var_name = node.left.value
        value = self.visit(node.right)
        self.symbol_table[var_name] = value
        return value

    def visit(self, node):
        method_name = f'visit_{node["type"]}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{node["type"]} method')

    def visit_INTEGER(self, node):
        return node['value']

    def visit_FLOAT(self, node):
        return node['value']

    def visit_STRING(self, node):
        return node['value']

    def visit_BOOLEAN(self, node):
        return node['value']

    def visit_IDENTIFIER(self, node):
        return node['value']

    def visit_LIST_EXPR(self, node):
        return [self.visit(element) for element in node['elements']]

    def visit_DICT_EXPR(self, node):
        return {key: self.visit(value) for key, value in node['pairs']}

    def visit_ASSIGN(self, node):
        value = self.visit(node['right'])
        var_name = node['left'].value  # Assuming Var has an attribute `value`
        self.symbol_table.set(var_name, value)  # Update the symbol table
        return value

    def visit_BINARY_OP(self, node):
        left = self.visit(node['left'])
        right = self.visit(node['right'])
        if node['op'] == TokenType.PLUS:
            return left + right
        elif node['op'] == TokenType.MINUS:
            return left - right
        elif node['op'] == TokenType.MUL:
            return left * right
        elif node['op'] == TokenType.DIV:
            return left / right
        elif node['op'] == TokenType.EQ:
            return left == right
        elif node['op'] == TokenType.NE:
            return left != right
        elif node['op'] == TokenType.LT:
            return left < right
        elif node['op'] == TokenType.LE:
            return left <= right
        elif node['op'] == TokenType.GT:
            return left > right
        elif node['op'] == TokenType.GE:
            return left >= right

    def visit_IF(self, node):
        if self.visit(node['condition']):
            return self.visit(node['if_body'])
        for elif_condition, elif_body in node['elif_blocks']:
            if self.visit(elif_condition):
                return self.visit(elif_body)
        if node['else_block']:
            return self.visit(node['else_block'])

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
