"""The parsers' package."""

from typing import Dict, Type

from pytkdocs.parsers.docstrings.base import Parser
from pytkdocs.parsers.docstrings.google import Google

PARSERS: Dict[str, Type[Parser]] = {"google": Google}
