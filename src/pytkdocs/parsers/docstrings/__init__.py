"""The parsers' package."""

from pytkdocs.parsers.docstrings.base import Parser, UnavailableParser
from pytkdocs.parsers.docstrings.google import Google
from pytkdocs.parsers.docstrings.markdown import Markdown
from pytkdocs.parsers.docstrings.restructured_text import RestructuredText

try:
    from pytkdocs.parsers.docstrings.numpy import Numpy
except ImportError:
    Numpy = UnavailableParser(  # type: ignore[misc,assignment]
        "pytkdocs must be installed with 'numpy-style' extra to parse Numpy docstrings",
    )


PARSERS: dict[str, type[Parser]] = {
    "google": Google,
    "restructured-text": RestructuredText,
    "numpy": Numpy,
    "markdown": Markdown,
}
