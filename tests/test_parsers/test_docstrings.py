"""Tests for [the `parsers.docstrings` module][pytkdocs.parsers.docstrings]."""

import inspect
from textwrap import dedent

from pytkdocs.loader import Loader
from pytkdocs.parsers.docstrings import parse as _parse


def parse(docstring, signature=None, return_type=inspect.Signature.empty, admonitions=True):
    return _parse("o", dedent(docstring).strip(), signature, return_type, admonitions)


def test_simple_docstring():
    sections, errors = parse("A simple docstring.")
    assert len(sections) == 1
    assert not errors


def test_multi_line_docstring():
    sections, errors = parse(
        """
        A somewhat longer docstring.

        Blablablabla.
        """
    )
    assert len(sections) == 1
    assert not errors


def test_sections_without_signature():
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


def test_property_docstring():
    class_ = Loader().get_object_documentation("tests.fixtures.parsing.docstrings.NotDefinedYet")
    prop = class_.attributes[0]
    sections, errors = prop.docstring_sections, prop.docstring_errors
    assert len(sections) == 2
    assert not errors


def test_function_without_annotations():
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


def test_function_with_annotations():
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


def test_types_in_docstring():
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

    x, y = sections[1].value
    r = sections[2].value

    assert x.name == "x"
    assert x.annotation == "int"
    assert x.description == "X value."
    assert x.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert x.default is inspect.Signature.empty

    assert y.name == "y"
    assert y.annotation == "int"
    assert y.description == "Y value."
    assert y.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert y.default is inspect.Signature.empty

    assert r.annotation == "int"
    assert r.description == "Sum X + Y."


def test_types_and_optional_in_docstring():
    def f(x=1, y=None):
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

    x, y = sections[1].value

    assert x.name == "x"
    assert x.annotation == "int"
    assert x.description == "X value."
    assert x.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert x.default == 1

    assert y.name == "y"
    assert y.annotation == "int"
    assert y.description == "Y value."
    assert y.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert y.default is None


def test_types_in_signature_and_docstring():
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


def test_close_sections():
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


def test_code_blocks():
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


def test_indented_code_block():
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


def test_extra_parameter():
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


def test_missing_parameter():
    def f(x, y):
        """
        Parameters:
            x: Integer.
        """
        return x + y

    sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
    assert len(sections) == 1
    assert not errors


def test_param_line_without_colon():
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


def test_admonitions():
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


def test_invalid_sections():
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


def test_multiple_lines_in_sections_items():
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
    assert len(sections[1].value) == 2
    assert errors
    for error in errors:
        assert "should be 4 * 2 = 8 spaces, not" in error


def test_parse_args_kwargs():
    def f(a, *args, **kwargs):
        """
        Arguments:
            a: a parameter.
            *args: args parameters.
            **kwargs: kwargs parameters.
        """
        return 1

    sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
    assert len(sections) == 1
    expected_parameters = {"a": "a parameter.", "*args": "args parameters.", "**kwargs": "kwargs parameters."}
    for param in sections[0].value:
        assert param.name in expected_parameters
        assert expected_parameters[param.name] == param.description
    assert not errors


def test_different_indentation():
    def f():
        """
        Hello.

        Raises:
             StartAt5: this section's items starts with 5 spaces of indentation.
                  Well indented continuation line.
              Badly indented continuation line (will trigger an error).

                      Empty lines are preserved, as well as extra-indentation (this line is a code block).
             AnyOtherLine: ...starting with exactly 5 spaces is a new item.
            AnyLine: ...indented with less than 5 spaces signifies the end of the section.
        """

    sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
    assert len(sections) == 3
    assert len(sections[1].value) == 2
    assert sections[1].value[0].description == (
        "this section's items starts with 5 spaces of indentation.\n"
        "Well indented continuation line.\n"
        "Badly indented continuation line (will trigger an error).\n"
        "\n"
        "    Empty lines are preserved, as well as extra-indentation (this line is a code block)."
    )
    assert sections[2].value == "    AnyLine: ...indented with less than 5 spaces signifies the end of the section."
    assert len(errors) == 1
    assert "should be 5 * 2 = 10 spaces, not 6" in errors[0]
