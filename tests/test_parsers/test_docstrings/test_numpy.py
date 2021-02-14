"""Tests for [the `parsers.docstrings.numpy` module][pytkdocs.parsers.docstrings.numpy]."""

import inspect
from textwrap import dedent

from pytkdocs.loader import Loader
from pytkdocs.parsers.docstrings.numpy import Numpy


class DummyObject:
    path = "o"


def parse(docstring, signature=None, return_type=inspect.Signature.empty):
    """Helper to parse a doctring."""
    return Numpy().parse(
        dedent(docstring).strip(),
        {"obj": DummyObject(), "signature": signature, "type": return_type},
    )


def test_simple_docstring():
    """Parse a simple docstring."""
    sections, errors = parse("A simple docstring.")
    assert len(sections) == 1
    assert not errors


def test_multi_line_docstring():
    """Parse a multi-line docstring."""
    sections, errors = parse(
        """
        A somewhat longer docstring.

        Blablablabla.
        """
    )
    assert len(sections) == 1
    assert not errors


def test_sections_without_signature():
    """Parse a docstring without a signature."""
    # type of return value always required
    sections, errors = parse(
        """
        Sections without signature.

        Parameters
        ----------
        void : 
            SEGFAULT.
        niet : 
            SEGFAULT.
        nada : 
            SEGFAULT.
        rien : 
            SEGFAULT.

        Raises
        ------
        GlobalError
            when nothing works as expected.

        Returns
        ------- 
        bool
            Itself.
        """
    )
    assert len(sections) == 4
    assert len(errors) == 4  # missing annotations for params
    for error in errors:
        assert "param" in error


def test_property_docstring():
    """Parse a property docstring."""
    class_ = Loader().get_object_documentation("tests.fixtures.parsing.docstrings.NotDefinedYet")
    prop = class_.attributes[0]
    sections, errors = prop.docstring_sections, prop.docstring_errors
    assert len(sections) == 2
    assert not errors


def test_function_without_annotations():
    """Parse a function docstring without signature annotations."""

    def f(x, y):
        """
        This function has no annotations.

        Parameters
        ----------
        x:
            X value.
        y:
            Y value.

        Returns
        -------
        float
            Sum X + Y.
        """
        return x + y

    sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
    assert len(sections) == 3
    assert not errors


def test_function_with_annotations():
    """Parse a function docstring with signature annotations."""

    def f(x: int, y: int) -> int:
        """
        This function has annotations.

        Parameters
        ----------
        x:
            X value.
        y:
            Y value.

        Returns
        -------
        int
            Sum X + Y.
        """
        return x + y

    sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
    assert len(sections) == 3
    assert not errors


def test_function_with_examples():
    """Parse a function docstring with signature annotations."""

    def f(x: int, y: int) -> int:
        """
        This function has annotations.

        Examples
        --------
        Some examples that will create an unified code block:

        >>> 2 + 2 == 5
        False
        >>> print("examples")
        "examples"

        This is just a random comment in the examples section.

        These examples will generate two different code blocks. Note the blank line.

        >>> print("I'm in the first code block!")
        "I'm in the first code block!"

        >>> print("I'm in other code block!")
        "I'm in other code block!"

        We also can write multiline examples:

        >>> x = 3 + 2
        >>> y = x + 10
        >>> y
        15

        This is just a typical Python code block:

        ```python
        print("examples")
        return 2 + 2
        ```

        Even if it contains doctests, the following block is still considered a normal code-block.

        ```python
        >>> print("examples")
        "examples"
        >>> 2 + 2
        4
        ```

        The blank line before an example is optional.
        >>> x = 3
        >>> y = "apple"
        >>> z = False
        >>> l = [x, y, z]
        >>> my_print_list_function(l)
        3
        "apple"
        False
        """
        return x + y

    sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
    assert len(sections) == 2
    assert len(sections[1].value) == 9
    assert not errors


def test_types_in_docstring():
    """Parse types in docstring."""

    def f(x, y):
        """
        The types are written in the docstring.

        Parameters
        ----------
        x : int
            X value.
        y : int
            Y value.

        Returns
        -------
        int
            Sum X + Y.
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
    """Parse optional types in docstring."""

    def f(x=1, y=None):
        """
        The types are written in the docstring.

        Parameters
        ----------
        x : int
            X value.
        y : int, optional
            Y value.

        Returns
        -------
        int
            Sum X + Y.
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
    """Parse types in both signature and docstring."""

    def f(x: int, y: int) -> int:
        """
        The types are written both in the signature and in the docstring.

        Parameters
        ----------
        x : int
            X value.
        y : int
            Y value.

        Returns
        -------
        int
            Sum X + Y.
        """
        return x + y

    sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
    assert len(sections) == 3
    assert not errors


def test_close_sections():
    """Parse sections without blank lines in between."""

    def f(x, y, z):
        """
        Parameters
        ----------
        x :
            X
        y :
            Y
        z :
            Z
        Raises
        ------
        Error2
            error.
        Error1
            error.
        Returns
        -------
        str
            value
        """
        return x + y + z

    sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
    assert len(sections) == 3
    assert not errors


# test_code_blocks was removed as docstrings within a code block
# are not applicable to numpy docstrings


def test_extra_parameter():
    """Warn on extra parameter in docstring."""

    def f(x):
        """
        Parameters
        ----------
        x :
            Integer.
        y :
            Integer.
        """
        return x

    sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
    assert len(sections) == 1
    assert len(errors) == 1
    assert "No type" in errors[0]


def test_missing_parameter():
    """Don't warn on missing parameter in docstring."""
    # FIXME: could warn
    def f(x, y):
        """
        Parameters
        ----------
        x :
            Integer.
        """
        return x + y

    sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
    assert len(sections) == 1
    assert not errors


def test_multiple_lines_in_sections_items():
    """Parse multi-line item description."""

    def f(p: str, q: str):
        """
        Hi.

        Parameters
        ----------
        p :
            This argument
            has a description
            spawning on multiple lines.

            It even has blank lines in it.
                    Some of these lines
                are indented for no reason.
        q :
            What if the first line is blank?
        """
        return p + q

    sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
    assert len(sections) == 2
    assert len(sections[1].value) == 2
    # numpy docstrings parameter description can be parsed even if misindentated
    assert not errors


def test_parse_args_kwargs():
    """Parse args and kwargs."""

    def f(a, *args, **kwargs):
        """
        Parameters
        ----------
        a :
            a parameter.
        *args :
            args parameters.
        **kwargs :
            kwargs parameters.
        """
        return 1

    sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
    assert len(sections) == 1
    expected_parameters = {
        "a": "a parameter.",
        "*args": "args parameters.",
        "**kwargs": "kwargs parameters.",
    }
    for param in sections[0].value:
        assert param.name in expected_parameters
        assert expected_parameters[param.name] == param.description
    assert not errors


def test_different_indentation():
    """Parse different indentations, warn on confusing indentation."""

    def f():
        """
        Hello.

        Raises
        ------
        StartAt5
            this section's items starts with x spaces of indentation.
            Well indented continuation line.
             Badly indented continuation line (will not trigger an error).

                Empty lines are preserved, as well as extra-indentation (this line is a code block).
        AnyOtherLine
            ...starting with exactly 5 spaces is a new item.
        """

    sections, errors = parse(inspect.getdoc(f), inspect.signature(f))
    assert len(sections) == 2
    assert len(sections[1].value) == 2
    assert sections[1].value[0].description == (
        "this section's items starts with x spaces of indentation.\n"
        "Well indented continuation line.\n"
        " Badly indented continuation line (will not trigger an error).\n"
        "\n"
        "    Empty lines are preserved, as well as extra-indentation (this line is a code block)."
    )
    assert not errors
