#!/usr/bin/env python
"""Scan Python files to retrieve real-world type annotations."""

import ast
import glob
import re
import sys
from multiprocessing import Pool, cpu_count
from pathlib import Path
from typing import List

try:
    from ast import unparse  # type: ignore
except ImportError:
    from astunparse import unparse as _unparse

    unparse = lambda node: _unparse(node).rstrip("\n").replace("(", "").replace(")", "")

regex = re.compile(r"\w+")


def scan_file(filepath: str) -> set:
    """
    Scan a Python file and return a set of annotations.

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
    except:
        return annotations
    for node in ast.walk(code):
        if hasattr(node, "annotation"):
            try:
                unparsed = unparse(node.annotation)  # type: ignore
                annotations.add(regex.sub("a", unparsed))
            except:
                continue
    return annotations


def main(directories: List[str]) -> int:
    """
    Scan Python files in a list of directories.

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
    n_files = len(all_files)
    with Pool(cpu_count() - 1) as pool:
        sets = pool.map(scan_file, all_files)
    annotations: set = set().union(*sets)
    print("a: " + "\na: ".join(sorted(annotations)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
