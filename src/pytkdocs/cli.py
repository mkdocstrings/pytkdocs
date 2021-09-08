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
import json
from typing import List, Optional

from pytkdocs.extensions.base import Extensions
from pytkdocs.json import Encoder
from pytkdocs.loader import Loader


def get_parser() -> argparse.ArgumentParser:
    """
    Return the program argument parser.

    Returns:
        The argument parser for the program.
    """
    parser = argparse.ArgumentParser(prog="pytkdocs")
    parser.add_argument("packages", metavar="PACKAGE", nargs="+", help="Packages to find and parse.")
    return parser


def p(objs, indent=""):
    s = 0
    for obj in objs:
        print(indent + repr(obj))
        s += 1
        s += p(obj.members.values(), indent + "  ")
    return s


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
    loader = Loader(extensions=extensions)
    modules = []
    for package in opts.packages:
        modules.append(loader.load_module(package))
    # p(modules)
    # print("-------------------------------")
    serialized = json.dumps(modules, cls=Encoder, indent=2, full=True)
    print(serialized)
    # print("-------------------------------")
    # deserialized = json.loads(serialized, object_hook=decoder)
    # p(deserialized)
    return 0
