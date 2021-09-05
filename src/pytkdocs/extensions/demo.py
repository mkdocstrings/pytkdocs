import ast

from pytkdocs.extensions.base import Extension


class ClassStartsAtOddLineNumberExtension(Extension):
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        if node.lineno % 2 == 1:
            self.visitor.current.labels.add("starts at odd line number")
