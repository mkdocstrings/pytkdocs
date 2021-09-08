import ast
from collections import defaultdict

from pytkdocs.dataclasses import Class, Function, Module


class Node:
    def __init__(self, ast_node, parent=None) -> None:
        self.node = ast_node
        self.parent = parent
        self.children = []

    def graft(self, ast_node):
        node = Node(ast_node, self)
        self.children.append(node)
        return node


class Tree:
    def __init__(self) -> None:
        self.node = None

    def graft(self, ast_node):
        self.node = Node(ast_node, self)
        return self.node


def visit(
    module_name,
    filepath,
    code,
    extensions,
):
    module = Module(module_name, filepath=filepath)
    # instantiating the visitor side-effects the module,
    # populating its members
    visitor = _Visitor(module, ast.parse(code), extensions)
    del visitor
    return module


class _Visitor(ast.NodeVisitor):
    def __init__(self, module, base_node, extensions) -> None:
        super().__init__()
        self.extensions = extensions.instantiate(self)
        self.scope = defaultdict(dict)
        self.current = module
        self.tree = Tree()
        self.node = self.tree
        self.generic_visit(base_node)

    def visit(self, node: ast.AST) -> None:
        self.node = self.node.graft(node)
        for pre_visitor in self.extensions.pre_visitors:
            pre_visitor.visit(node)
        super().visit(node)
        for post_visitor in self.extensions.post_visitors:
            post_visitor.visit(node)
        self.node = self.node.parent

    def visit_Import(self, node):
        # for alias in node.names:
        #     self.scope[self.path][alias.asname or alias.name] = alias.name
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        # for alias in node.names:
        #     self.scope[self.path][alias.asname or alias.name] = f"{node.module}.{alias.name}"
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if node.decorator_list:
            lineno = node.decorator_list[0].lineno
        else:
            lineno = node.lineno
        function = Function(node.name, lineno=lineno, endlineno=node.end_lineno)
        self.current[node.name] = function

    def visit_ClassDef(self, node):
        class_ = Class(node.name, lineno=node.lineno, endlineno=node.end_lineno)
        self.current[node.name] = class_
        self.current = class_
        self.generic_visit(node)
        self.current = self.current.parent
