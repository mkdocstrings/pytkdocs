"""This module defines functions and classes to parse docstrings into structured data."""

from typing import List

from pytkdocs.parsers.docstrings.base import Parser, Section


class Markdown(Parser):
    """A Markdown docstrings parser."""

    def parse_sections(self, docstring: str) -> List[Section]:  # noqa: D102
        return [Section(Section.Type.MARKDOWN, docstring)]
