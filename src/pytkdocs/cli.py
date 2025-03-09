"""Module that contains the command line application."""

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

from __future__ import annotations

import argparse
import json
import sys
import traceback
from contextlib import contextmanager
from io import StringIO
from typing import TYPE_CHECKING, Any

from pytkdocs import debug
from pytkdocs.loader import Loader
from pytkdocs.serializer import serialize_object

if TYPE_CHECKING:
    from collections.abc import Iterator

    from pytkdocs.objects import Object


class _DebugInfo(argparse.Action):
    def __init__(self, nargs: int | str | None = 0, **kwargs: Any) -> None:
        super().__init__(nargs=nargs, **kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        debug.print_debug_info()
        sys.exit(0)


def process_config(config: dict) -> dict:
    """Process a loading configuration.

    The `config` argument is a dictionary looking like this:

    ```python
    {
        "objects": [
            {"path": "python.dotted.path.to.the.object1"},
            {"path": "python.dotted.path.to.the.object2"},
        ]
    }
    ```

    The result is a dictionary looking like this:

    ```python
    {
        "loading_errors": [
            "message1",
            "message2",
        ],
        "parsing_errors": {
            "path.to.object1": [
                "message1",
                "message2",
            ],
            "path.to.object2": [
                "message1",
                "message2",
            ],
        },
        "objects": [
            {
                "path": "path.to.object1",
                # other attributes, see the documentation for `pytkdocs.objects` or `pytkdocs.serializer`
            },
            {
                "path": "path.to.object2",
                # other attributes, see the documentation for `pytkdocs.objects` or `pytkdocs.serializer`
            },
        ],
    }
    ```

    Arguments:
        config: The configuration.

    Returns:
        The collected documentation along with the errors that occurred.
    """
    collected = []
    loading_errors = []
    parsing_errors = {}

    for obj_config in config["objects"]:
        path = obj_config.pop("path")
        members = obj_config.pop("members", set())

        if isinstance(members, list):
            members = set(members)
        loader = Loader(**obj_config)

        obj = loader.get_object_documentation(path, members)

        loading_errors.extend(loader.errors)
        parsing_errors.update(extract_errors(obj))

        serialized_obj = serialize_object(obj)
        collected.append(serialized_obj)

    return {"loading_errors": loading_errors, "parsing_errors": parsing_errors, "objects": collected}


def process_json(json_input: str) -> dict:
    """Process JSON input.

    Simply load the JSON as a Python dictionary, then pass it to [`process_config`][pytkdocs.cli.process_config].

    Arguments:
        json_input: The JSON to load.

    Returns:
        The result of the call to [`process_config`][pytkdocs.cli.process_config].
    """
    return process_config(json.loads(json_input))


def extract_docstring_parsing_errors(errors: dict, obj: Object) -> None:
    """Recursion helper.

    Update the `errors` dictionary by side-effect. Recurse on the object's children.

    Arguments:
        errors: The dictionary to update.
        obj: The object.
    """
    if hasattr(obj, "docstring_errors") and obj.docstring_errors:
        errors[obj.path] = obj.docstring_errors
    for child in obj.children:
        extract_docstring_parsing_errors(errors, child)


def extract_errors(obj: Object) -> dict:
    """Extract the docstring parsing errors of each object, recursively, into a flat dictionary.

    Arguments:
        obj: An object from `pytkdocs.objects`.

    Returns:
        A flat dictionary. Keys are the objects' names.
    """
    parsing_errors: dict[str, list[str]] = {}
    extract_docstring_parsing_errors(parsing_errors, obj)
    return parsing_errors


def get_parser() -> argparse.ArgumentParser:
    """Return the program argument parser.

    Returns:
        The argument parser for the program.
    """
    parser = argparse.ArgumentParser(prog="pytkdocs")
    parser.add_argument(
        "-1",
        "--line-by-line",
        action="store_true",
        dest="line_by_line",
        help="Process each line read on stdin, one by one.",
    )
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {debug.get_version()}")
    parser.add_argument("--debug-info", action=_DebugInfo, help="Print debug information.")
    return parser


@contextmanager
def discarded_stdout() -> Iterator[None]:
    """Discard standard output.

    Yields:
        Nothing: We only yield to act as a context manager.
    """
    # Discard things printed at import time to avoid corrupting our JSON output
    # See https://github.com/pawamoy/pytkdocs/issues/24
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    yield

    # Flush imported modules' output, and restore true sys.stdout
    sys.stdout.flush()
    sys.stdout = old_stdout


def main(args: list[str] | None = None) -> int:
    """Run the main program.

    This function is executed when you type `pytkdocs` or `python -m pytkdocs`.

    Parameters:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    parsed_args: argparse.Namespace = parser.parse_args(args)

    if parsed_args.line_by_line:
        for line in sys.stdin:
            with discarded_stdout():
                try:
                    output = json.dumps(process_json(line))
                except Exception as error:  # noqa: BLE001
                    # Don't fail on error. We must handle the next inputs.
                    # Instead, print error as JSON.
                    output = json.dumps({"error": str(error), "traceback": traceback.format_exc()})
            print(output)
    else:
        with discarded_stdout():
            output = json.dumps(process_json(sys.stdin.read()))
        print(output)

    return 0
