"""This module defines functions and classes to parse docstrings into structured data."""

from pytkdocs.parsers.docstrings.base import Parser, Section


class Markdown(Parser):
    """A Markdown docstrings parser."""

    def parse_sections(self, docstring: str) -> list[Section]:  # noqa: D102
        return [Section(Section.Type.MARKDOWN, docstring)]
