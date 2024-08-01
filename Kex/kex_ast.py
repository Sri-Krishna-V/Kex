# Purpose: AST classes for the Kex language
# Detailed working of kex_ast class: The AST classes represent the nodes of the Abstract Syntax Tree (AST) that is generated by the parser during the parsing process. Each AST class corresponds to a different type of node in the AST, such as binary operations, numbers, variables, assignments, lists, dictionaries, if statements, and blocks of statements.
# The AST classes define the structure of the nodes in the AST and provide methods for creating, manipulating, and traversing the AST. The AST classes are used by the parser to construct the AST from the tokens generated by the lexer and represent the program logic in a hierarchical tree structure.
# The AST classes implement methods for comparing, hashing, and string representation of the nodes to facilitate debugging, testing, and visualization of the AST. They also define special methods for arithmetic operations, logical operations, and other operations that can be performed on the AST nodes.
# The AST classes are an essential component of the Kex interpreter as they represent the program structure and logic in a format that can be easily processed and executed by the interpreter. They provide a high-level abstraction of the program code and enable the interpreter to evaluate expressions, execute statements, and control the flow of the program based on the AST nodes.
# The AST classes are designed to be extensible and flexible, allowing for the addition of new node types and features to support the evolving requirements of the Kex language. They provide a foundation for building complex programs and applications using the Kex language and enable developers to create expressive, readable, and maintainable code.


import math
from kex_tokens import Token, TokenType


class AST:
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

    def __str__(self):
        return f"{self.left} {self.op} {self.right}"

    def __eq__(self, other):
        if isinstance(other, BinOp):
            return self.left == other.left and self.op == other.op and self.right == other.right
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.left, self.op, self.right))

    def __lt__(self, other):
        return self.left < other.left and self.op < other.op and self.right < other.right

    def __le__(self, other):
        return self.left <= other.left and self.op <= other.op and self.right <= other.right

    def __gt__(self, other):
        return self.left > other.left and self.op > other.op and self.right > other.right

    def __ge__(self, other):
        return self.left >= other.left and self.op >= other.op and self.right >= other.right

    def __len__(self):
        return len(self.left) + len(self.op) + len(self.right)

    def __getitem__(self, index):
        return [self.left, self.op, self.right][index]

    def __iter__(self):
        return iter([self.left, self.op, self.right])

    def __contains__(self, item):
        return item in [self.left, self.op, self.right]

    def __add__(self, other):
        if isinstance(other, BinOp):
            return BinOp(self.left + other.left, self.op + other.op, self.right + other.right)

        return BinOp(self.left + other, self.op, self.right)


class String(AST):
    def __init__(self, token):
        self.value = token.value

    def __repr__(self):
        return f"String({self.value})"

    def __str__(self):
        return f"{self.value}"

    def __eq__(self, other):
        if isinstance(other, String):
            return self.value == other.value
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


class Boolean(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"Boolean({self.value})"

    def __str__(self):
        return f"{self.value}"

    def __eq__(self, other):
        if isinstance(other, Boolean):
            return self.value == other.value
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


class Num(AST):
    def __init__(self, token):
        self.value = token.value

    def __repr__(self):
        return f"Num({self.value})"

    def __str__(self):
        return f"{self.value}"


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"Var({self.value})"

    def __str__(self):
        return f"{self.value}"


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self):
        return f"Assign({self.left}, {self.op}, {self.right})"

    def __str__(self):
        return f"{self.left} {self.op} {self.right}"


class ListExpr(AST):
    def __init__(self, elements):
        self.elements = elements


class DictExpr(AST):
    def __init__(self, pairs):
        self.pairs = pairs


class If(AST):
    def __init__(self, condition, if_body, elif_blocks, else_body):
        self.condition = condition
        self.if_body = if_body
        self.elif_blocks = elif_blocks  # List of (condition, body) tuples
        self.else_body = else_body

    def __repr__(self):
        return f"If(condition={self.condition}, if_body={self.if_body}, elif_blocks={self.elif_blocks}, else_body={self.else_body})"

    def __str__(self):
        return f"If {self.condition} {self.if_body} {self.elif_blocks} {self.else_body}"


class Block(AST):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"

    def __str__(self):
        return f"{self.statements}"

    def __eq__(self, other):
        if isinstance(other, Block):
            return self.statements == other.statements
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.statements)


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def get(self, name):
        return self.symbols.get(name)

    def set(self, name, value):
        self.symbols[name] = value

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, value):
        self.set(name, value)

    def __contains__(self, name):
        return name in self.symbols

    def __repr__(self):
        return f"SymbolTable({self.symbols})"

    def __str__(self):
        return f"{self.symbols}"

    def __len__(self):
        return len(self.symbols)

    def __iter__(self):
        return iter(self.symbols)

    def __eq__(self, other):
        if isinstance(other, SymbolTable):
            return self.symbols == other.symbols
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.symbols)

    def __bool__(self):
        return bool(self.symbols)

    def __add__(self, other):
        if isinstance(other, SymbolTable):
            return SymbolTable(self.symbols + other.symbols)
        return SymbolTable(self.symbols + other)

    def __sub__(self, other):
        if isinstance(other, SymbolTable):
            return SymbolTable(self.symbols - other.symbols)
        return SymbolTable(self.symbols - other)

    def __mul__(self, other):
        if isinstance(other, SymbolTable):
            return SymbolTable(self.symbols * other.symbols)
        return SymbolTable(self.symbols * other)

    def __floordiv__(self, other):
        if isinstance(other, SymbolTable):
            return SymbolTable(self.symbols // other.symbols)
        return SymbolTable(self.symbols // other)

    def __truediv__(self, other):
        if isinstance(other, SymbolTable):
            return SymbolTable(self.symbols / other.symbols)
        return SymbolTable(self.symbols / other)

    def __mod__(self, other):
        if isinstance(other, SymbolTable):
            return SymbolTable(self.symbols % other.symbols)
        return SymbolTable(self.symbols % other)

    def __pow__(self, other):
        if isinstance(other, SymbolTable):
            return SymbolTable(self.symbols ** other.symbols)
        return SymbolTable(self.symbols ** other)

    def __lshift__(self, other):
        if isinstance(other, SymbolTable):
            return SymbolTable(self.symbols << other.symbols)
        return SymbolTable(self.symbols << other)

    def __rshift__(self, other):
        if isinstance(other, SymbolTable):
            return SymbolTable(self.symbols >> other.symbols)
        return SymbolTable(self.symbols >> other)

    def __and__(self, other):
        if isinstance(other, SymbolTable):
            return SymbolTable(self.symbols & other.symbols)
        return SymbolTable(self.symbols & other)

    def __xor__(self, other):
        if isinstance(other, SymbolTable):
            return SymbolTable(self.symbols ^ other.symbols)
        return SymbolTable(self.symbols ^ other)

    def __or__(self, other):
        if isinstance(other, SymbolTable):
            return SymbolTable(self.symbols | other.symbols)
        return SymbolTable(self.symbols | other)

    def __neg__(self):
        return SymbolTable(-self.symbols)

    def __pos__(self):
        return SymbolTable(+self.symbols)

    def __abs__(self):
        return SymbolTable(abs(self.symbols))

    def __invert__(self):
        return SymbolTable(~self.symbols)

    def __round__(self, n=0):
        return SymbolTable(round(self.symbols, n))

    def __floor__(self):
        return SymbolTable(math.floor(self.symbols))

    def __ceil__(self):
        return SymbolTable(math.ceil(self.symbols))

    def __trunc__(self):
        return SymbolTable(math.trunc(self.symbols))

    def __lt__(self, other):
        return self.symbols < other.symbols

    def __le__(self, other):
        return self.symbols <= other.symbols

    def __eq__(self, other):
        return self.symbols == other.symbols

    def __ne__(self, other):
        return self.symbols != other.symbols

    def __gt__(self, other):
        return self.symbols > other.symbols

    def __ge__(self, other):
        return self.symbols >= other.symbols

    def __round__(self, n=0):
        return SymbolTable(round(self.symbols, n))

    def __floor__(self):
        return SymbolTable(math.floor(self.symbols))

    def __ceil__(self):
        return SymbolTable(math.ceil(self.symbols))

    def __trunc__(self):
        return SymbolTable(math.trunc(self.symbols))

    def __add__(self, other):
        return self.symbols + other.symbols
