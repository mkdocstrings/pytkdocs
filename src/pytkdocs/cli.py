"""
Module that contains the command line application.

Why does this file exist, and why not put this in __main__?

You might be tempted to import things from __main__ later,
but that will cause problems: the code will get executed twice:

- When you run `python -m pytkdocs` python will execute
  ``__main__.py`` as a script. That means there won't be any
  ``pytkdocs.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``pytkdocs.__main__`` in ``sys.modules``.

Also see http://click.pocoo.org/5/setuptools/#setuptools-integration.
"""
import argparse
import json
import sys
import traceback

from .loader import Loader
from .serializer import serialize_object


def process_json(json_input):
    return process_config(json.loads(json_input))


def process_config(config):
    global_config = config["global_config"]
    collected = []
    loading_errors = []
    parsing_errors = {}

    for obj in config["objects"]:
        loader_config = dict(global_config)
        loader_config.update(obj["config"])
        loader = Loader(**loader_config)

        obj = loader.get_object_documentation(obj["path"])

        loading_errors.extend(loader.errors)
        parsing_errors.update(extract_errors(obj))

        serialized_obj = serialize_object(obj)
        collected.append(serialized_obj)

    print(json.dumps(dict(loading_errors=loading_errors, parsing_errors=parsing_errors, objects=collected)))


def extract_docstring_parsing_errors(errors, o):
    if o.docstring.parsing_errors:
        errors[o.path] = o.docstring.parsing_errors
    for child in o.children:
        extract_docstring_parsing_errors(errors, child)


def extract_errors(obj):
    parsing_errors = {}
    extract_docstring_parsing_errors(parsing_errors, obj)
    return parsing_errors


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-1",
        "--line-by-line",
        action="store_true",
        dest="line_by_line",
        help="Process each line read on stdin, one by one.",
    )
    return parser


def main():
    """The main function, which is executed when you type ``pytkdocs`` or ``python -m pytkdocs``."""
    parser = get_parser()
    args = parser.parse_args()

    if args.line_by_line:
        for line in sys.stdin:
            try:
                process_json(line)
            except Exception as error:
                # Don't fail on error. We must handle the next inputs.
                # Instead, print error as JSON.
                print(json.dumps({"error": str(error), "traceback": traceback.format_exc()}))
    else:
        process_json(sys.stdin.read())

    return 0
