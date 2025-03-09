"""Tests for [the `parsers.attributes` module][pytkdocs.parsers.attributes] on annotations."""

import ast
from collections.abc import Iterator

import pytest

from pytkdocs.parsers.attributes import unparse_annotation


def annotations(annotations_file: str) -> Iterator[str]:
    with open(annotations_file) as fp:
        for line in fp:
            line = line.rstrip("\n")  # noqa: PLW2901
            yield line  # annotation
            yield line + " = 0"  # annotated assignment


@pytest.mark.parametrize("code", list(annotations("tests/fixtures/parsing/annotations.txt")))
def test_annotation_to_text(code: str) -> None:
    node = ast.parse(code, mode="single").body[0]
    assert unparse_annotation(node.annotation) == code[3:].replace(" = 0", "")  # type: ignore[attr-defined]
