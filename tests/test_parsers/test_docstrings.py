"""Tests for [the `parsers.docstrings` module][pytkdocs.parsers.docstrings]."""

import inspect
from textwrap import dedent

from pytkdocs.loader import Loader
from pytkdocs.parsers.docstrings import parse as _parse


def parse(docstring, signature=None, return_type=inspect.Signature.empty, admonitions=True):
    return _parse("o", dedent(docstring).strip(), signature, return_type, admonitions)


class TestDocstringParser:
    def test_simple_docstring(self):
        sections, errors = parse("A simple docstring.")
        assert len(sections) == 1
        assert not errors

    def test_multi_line_docstring(self):
        sections, errors = parse(
            """
            A somewhat longer docstring.

            Blablablabla.
            """
        )
        assert len(sections) == 1
        assert not errors

    def test_sections_without_signature(self):
        sections, errors = parse(
            """
            Sections without signature.

            Parameters:
                void: SEGFAULT.
                niet: SEGFAULT.
                nada: SEGFAULT.
                rien: SEGFAULT.

            Exceptions:
                GlobalError: when nothing works as expected.

            Returns:
                Itself.
            """
        )

        assert len(sections) == 4
        assert len(errors) == 5  # missing annotations for params and return
        for error in errors[:-1]:
            assert "param" in error
        assert "return" in errors[-1]

    def test_property_docstring(self):
        class_ = Loader().get_object_documentation("tests.fixtures.parsing.docstrings.NotDefinedYet")
        prop = class_.attributes[0]
        sections, errors = prop.docstring_sections, prop.docstring_errors
        assert len(sections) == 2
        assert not errors

    def test_function_without_annotations(self):
        def f(x, y):
            """
            This function has no annotations.

            Parameters:
                x: X value.
                y: Y value.

            Returns:
                Sum X + Y.
            """
            return x + y

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert len(sections) == 3
        assert len(errors) == 1
        assert "No type in return" in errors[0]

    def test_function_with_annotations(self):
        def f(x: int, y: int) -> int:
            """
            This function has annotations.

            Parameters:
                x: X value.
                y: Y value.

            Returns:
                Sum X + Y.
            """
            return x + y

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert len(sections) == 3
        assert not errors

    def test_types_in_docstring(self):
        def f(x, y):
            """
            The types are written in the docstring.

            Parameters:
                x (int): X value.
                y (int): Y value.

            Returns:
                int: Sum X + Y.
            """
            return x + y

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert len(sections) == 3
        assert not errors

    def test_types_and_optional_in_docstring(self):
        def f(x, y=None):
            """
            The types are written in the docstring.

            Parameters:
                x (int): X value.
                y (int, optional): Y value.

            Returns:
                int: Sum X + Y.
            """
            return x + (y or 1)

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert len(sections) == 3
        assert not errors

    def test_types_in_signature_and_docstring(self):
        def f(x: int, y: int) -> int:
            """
            The types are written both in the signature and in the docstring.

            Parameters:
                x (int): X value.
                y (int): Y value.

            Returns:
                int: Sum X + Y.
            """
            return x + y

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert len(sections) == 3
        assert not errors

    def test_close_sections(self):
        def f(x, y, z):
            """
            Parameters:
                x: X.
            Parameters:
                y: Y.

            Parameters:
                z: Z.
            Exceptions:
                Error2: error.
            Exceptions:
                Error1: error.
            Returns:
                1.
            Returns:
                2.
            """
            return x + y + z

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert len(sections) == 7
        assert len(errors) == 2  # no return type annotations

    def test_code_blocks(self):
        def f(s):
            """
            This docstring contains a docstring in a code block o_O!

            ```python
            \"\"\"
            This docstring is contained in another docstring O_o!

            Parameters:
                s: A string.
            \"\"\"
            ```
            """
            return s

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert len(sections) == 1
        assert not errors

    def test_indented_code_block(self):
        def f(s):
            """
            This docstring contains a docstring in a code block o_O!

                \"\"\"
                This docstring is contained in another docstring O_o!

                Parameters:
                    s: A string.
                \"\"\"
            """
            return s

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert len(sections) == 1
        assert not errors

    def test_extra_parameter(self):
        def f(x):
            """
            Parameters:
                x: Integer.
                y: Integer.
            """
            return x

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert len(sections) == 1
        assert len(errors) == 1
        assert "No type" in errors[0]

    def test_missing_parameter(self):
        def f(x, y):
            """
            Parameters:
                x: Integer.
            """
            return x + y

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert len(sections) == 1
        assert not errors

    def test_param_line_without_colon(self):
        def f(x: int):
            """
            Parameters:
                x is an integer.
            """
            return x

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert not sections  # getting x fails, so the section is empty and discarded
        assert len(errors) == 2
        assert "pair" in errors[0]
        assert "Empty" in errors[1]

    def test_admonitions(self):
        def f():
            """
            Note:
                Hello.

            Note: With title.
                Hello again.

            Something:
                Something.
            """

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert len(sections) == 1
        assert not errors

    def test_invalid_sections(self):
        def f():
            """
            Parameters:
            Exceptions:
            Exceptions:

            Returns:
            Note:

            Important:
            """

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert len(sections) == 1
        for error in errors[:3]:
            assert "Empty" in error
        assert "No return type" in errors[3]
        assert "Empty" in errors[-1]

    def test_multiple_lines_in_sections_items(self):
        def f(p: str, q: str):
            """
            Hi.

            Arguments:
                p: This argument
                   has a description
                  spawning on multiple lines.

                   It even has blank lines in it.
                           Some of these lines
                       are indented for no reason.
                q:
                  What if the first line is blank?
            """
            return p + q

        sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
        assert len(sections) == 2
        assert not errors
