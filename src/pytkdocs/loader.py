import sys
from pathlib import Path
from typing import List

from pytkdocs.collections import lines_collection
from pytkdocs.dataclasses import Module
from pytkdocs.visitor import visit


class Loader:
    def __init__(self, extensions) -> None:
        self.extensions = extensions

    def load_module(self, module_name, recursive=True):
        module_path = find_module(module_name)
        return self._load_module_path(module_name, module_path, recursive=recursive)

    def _load_module_path(self, module_name, module_path, recursive=True):
        code = module_path.read_text()
        lines_collection[module_path] = code.splitlines(keepends=False)
        module = visit(
            module_name,
            filepath=module_path,
            code=code,
            extensions=self.extensions,
        )
        if recursive:
            for subparts, subpath in sorted(iter_submodules(module_path), key=lambda tup: len(tup[0])):
                parent_parts = subparts[:-1]
                try:
                    member_parent = module[parent_parts]
                except KeyError:
                    print(subpath, "is not importable, using folder", file=sys.stderr)
                    member_parent = Module(subpath.parent.name)
                    module[parent_parts] = member_parent
                member_parent[subparts[-1]] = self._load_module_path(subparts[-1], subpath, recursive=False)
        return module


# credits to @NiklasRosenstein and the docspec project
def find_module(module_name: str, search_path: List[str] = None) -> str:
    if search_path is None:
        search_path = sys.path

    # optimization: pre-compute Paths to relieve CPU when joining paths
    search_path = [Path(path) for path in search_path]
    parts = module_name.split(".")

    filenames = [
        Path(*parts, "__init__.py"),
        Path(*parts[:-1], f"{parts[-1]}.py"),
    ]

    for path in search_path:
        for choice in filenames:
            abs_path = path / choice
            # optimization: just check if the file exists,
            # not if it's an actual file
            if abs_path.exists():
                return abs_path

    raise ImportError(module_name)


def iter_submodules(path):
    if path.name == "__init__.py":
        path = path.parent
    # optimization: just check if the file name ends with .py
    # (to distinguish it from a directory),
    # not if it's an actual file
    elif path.suffix == ".py":
        return

    for subpath in path.rglob("*.py"):
        rel_subpath = subpath.relative_to(path)
        if rel_subpath.name == "__init__.py":
            # optimization: since it's a relative path,
            # if it has only one part and is named __init__.py,
            # it means it's the starting path
            # (no need to compare it against starting path)
            if len(rel_subpath.parts) == 1:
                continue
            yield rel_subpath.parts[:-1], subpath
        else:
            yield rel_subpath.with_suffix("").parts, subpath
