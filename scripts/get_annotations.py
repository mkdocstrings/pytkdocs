#!/usr/bin/env python
"""Scan Python files to retrieve real-world type annotations."""

import ast
import glob
import re
import sys
from multiprocessing import Pool, cpu_count
from pathlib import Path

try:
    from ast import unparse  # type: ignore[attr-defined]
except ImportError:
    from astunparse import unparse as _unparse  # type: ignore[no-redef]

    unparse = lambda node: _unparse(node).rstrip("\n").replace("(", "").replace(")", "")  # type: ignore[assignment]  # noqa: E731

regex = re.compile(r"\w+")


def scan_file(filepath: str) -> set:
    """Scan a Python file and return a set of annotations.

    Since parsing `Optional[typing.List]` and `Optional[typing.Dict]` is the same,
    we're not interested in keeping the actual names.
    Therefore we replace every word with "a".
    It has two benefits:

    - we can get rid of syntaxically equivalent annotations (duplicates)
    - the resulting annotations takes less bytes

    Arguments:
        filepath: The path to the Python file to scan.

    Returns:
        A set of annotations.
    """
    annotations: set = set()
    path = Path(filepath)
    try:
        code = ast.parse(path.read_text())
    except:  # noqa: E722
        return annotations
    for node in ast.walk(code):
        if hasattr(node, "annotation"):
            try:
                unparsed = unparse(node.annotation)
                annotations.add(regex.sub("a", unparsed))
            except:  # noqa: E722, S112
                continue
    return annotations


def main(directories: list[str]) -> int:
    """Scan Python files in a list of directories.

    First, all the files are stored in a list,
    then the scanning is done in parallel with a multiprocessing pool.

    Arguments:
        directories: A list of directories to scan.

    Returns:
        An exit code.
    """
    if not directories:
        return 1
    all_files = []
    for directory in directories:
        all_files.extend(glob.glob(directory.rstrip("/") + "/**/*.py", recursive=True))
    with Pool(cpu_count() - 1) as pool:
        sets = pool.map(scan_file, all_files)
    annotations: set = set().union(*sets)
    print("a: " + "\na: ".join(sorted(annotations)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
