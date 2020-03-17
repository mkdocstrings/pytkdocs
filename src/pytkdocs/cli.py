"""
Module that contains the command line application.

Why does this file exist, and why not put this in __main__?

You might be tempted to import things from __main__ later,
but that will cause problems: the code will get executed twice:

- When you run `python -m pydocload` python will execute
  ``__main__.py`` as a script. That means there won't be any
  ``pydocload.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``pydocload.__main__`` in ``sys.modules``.

Also see http://click.pocoo.org/5/setuptools/#setuptools-integration.
"""

import json
import sys

from .loader import Loader


def main():
    """The main function, which is executed when you type ``pydocload`` or ``python -m pydocload``."""
    process_each_line = True

    if process_each_line:
        for line in sys.stdin:
            process(line)
    else:
        process(sys.stdin.read())


def process(json_input):
    config = json.loads(json_input)
    global_config = config["global_config"]
    result = []
    for obj in config["objects"]:
        loader_config = dict(global_config)
        loader_config.update(obj["config"])
        loader = Loader(**loader_config)
        result.append(loader.get_object_documentation(obj["path"]).flatten())
    print(json.dumps(result))
    return 0
