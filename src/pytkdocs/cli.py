# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m pytkdocs` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `pytkdocs.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `pytkdocs.__main__` in `sys.modules`.

"""Module that contains the command line application."""

import argparse
import glob
import os
from typing import List, Optional

from pytkdocs.extensions.base import Extensions
from pytkdocs.extensions.demo import ClassStartsAtOddLineNumberExtension
from pytkdocs.parser import Parser


def find_modules(directory, recursive=True):
    expr = "**/*.py" if recursive else "*.py"
    yield from glob.glob(f"{directory}/{expr}", recursive=recursive)


def yield_modules_paths(paths, recursive=True):
    for path in paths:
        if os.path.isdir(path):
            yield from find_modules(path, recursive)
        else:
            yield path


def get_parser() -> argparse.ArgumentParser:
    """
    Return the program argument parser.

    Returns:
        The argument parser for the program.
    """
    parser = argparse.ArgumentParser(prog="pytkdocs")
    parser.add_argument("paths", metavar="PATH", nargs="+", help="Paths to parse (files or directories).")
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """
    Run the main program.

    This function is executed when you type `pytkdocs` or `python -m pytkdocs`.

    Arguments:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    opts: argparse.Namespace = parser.parse_args(args)  # type: ignore

    extensions = Extensions()
    extensions.add_post_visitor(ClassStartsAtOddLineNumberExtension)
    parser = Parser(extensions=extensions)
    modules = []
    for path in yield_modules_paths(opts.paths):
        modules.append(parser.parse_module(path))
    for module in modules:
        print(module.filepath)
    return 0
