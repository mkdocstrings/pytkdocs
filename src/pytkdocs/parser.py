import ast
from pathlib import Path

from pytkdocs.collections import lines_collection
from pytkdocs.dataclasses import Module
from pytkdocs.visitor import Visitor


class Parser:
    def __init__(self, extensions) -> None:
        self.extensions = extensions

    def parse_module(self, filepath):
        text = Path(filepath).read_text()
        lines_collection[filepath] = lines = text.splitlines(keepends=False)
        name = filepath.rsplit("/", 1)[1].rsplit(".", 1)[0]
        module = Module(filepath, name, starting_line=1, ending_line=len(lines) + 1)
        return Visitor(module, ast.parse(text), extensions=self.extensions).pop()
