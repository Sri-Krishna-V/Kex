# Purpose: NodeVisitor class for AST traversal
# Detailed working of kex_Nodevisitor : This class is used to traverse the AST. It has a visit method that takes a node as an argument and calls the appropriate visit method based on the type of the node. If a visit method for a specific node type is not defined, it raises an exception. The visit method returns the result of the appropriate visit method for the node.
# The NodeVisitor class defines visit methods for different types of AST nodes, such as Program, Block, Var, Assign, BinOp, Num, ListExpr, DictExpr, Boolean, and String. Each visit method is responsible for visiting the corresponding node and its children nodes in the AST. The visit method for each node type is implemented to handle the specific logic required to traverse that type of node.
# The NodeVisitor class is used by the Interpreter class to traverse the AST and execute the program logic. The Interpreter class calls the visit method of the NodeVisitor class for each node in the AST to interpret the program and evaluate the expressions and statements in the program. The NodeVisitor class provides a generic_visit method that raises an exception if a visit method for a specific node type is not defined, ensuring that all node types are handled correctly during AST traversal.

from kex_ast import AST, BinOp, Num, Var, Assign, ListExpr, DictExpr


class NodeVisitor:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Program(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_Block(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_Var(self, node):
        pass

    def visit_Assign(self, node):
        self.visit(node.right)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Num(self, node):
        pass

    def visit_ListExpr(self, node):
        for element in node.elements:
            self.visit(element)

    def visit_DictExpr(self, node):
        for key, value in node.pairs:
            self.visit(key)
            self.visit(value)

    def visit_Boolean(self, node):
        pass

    def visit_String(self, node):
        pass

    def visit_If(self, node):
        self.visit(node.condition)
        self.visit(node.if_body)
        for condition, body in node.elif_blocks:
            self.visit(condition)
            self.visit(body)
        self.visit(node.else_body)
