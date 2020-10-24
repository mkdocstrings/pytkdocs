"""Tests for [the `parsers.docstrings.google` module][pytkdocs.parsers.docstrings.google]."""

import inspect
from textwrap import dedent

import pytest

from pytkdocs.loader import Loader
from pytkdocs.objects import Object
from pytkdocs.parsers.docstrings.base import AnnotatedObject, Attribute, Parameter, Section, empty
from pytkdocs.parsers.docstrings.restructured_text import RestructuredText
from pytkdocs.serializer import serialize_attribute


class DummyObject:
    path = "o"


SOME_NAME = "foo"
SOME_TEXT = "descriptive test text"
SOME_EXTRA_TEXT = "more test text"
SOME_EXCEPTION_NAME = "SomeException"
SOME_OTHER_EXCEPTION_NAME = "SomeOtherException"


def dedent_strip(text: str) -> str:
    return dedent(text).strip()


def parse(obj):
    """Helper to parse a docstring."""
    return parse_detailed(inspect.getdoc(obj), inspect.signature(obj))


def parse_detailed(docstring, signature=None, return_type=inspect.Signature.empty):
    """Helper to parse a docstring."""
    return RestructuredText().parse(
        dedent_strip(docstring), {"obj": DummyObject(), "signature": signature, "type": return_type}
    )


def assert_parameter_equal(actual: Parameter, expected: Parameter) -> None:
    assert actual.name == expected.name
    assert_annotated_obj_equal(actual, expected)
    assert actual.kind == expected.kind
    assert actual.default == expected.default


def assert_attribute_equal(actual: Attribute, expected: Attribute) -> None:
    assert actual.name == expected.name
    assert_annotated_obj_equal(actual, expected)


def assert_annotated_obj_equal(actual: AnnotatedObject, expected: AnnotatedObject) -> None:
    assert actual.annotation == expected.annotation
    assert actual.description == expected.description


def get_rst_object_documentation(dotted_fixture_subpath) -> Object:
    return Loader(docstring_style="restructured-text").get_object_documentation(
        f"tests.fixtures.parsing.restructured_text.{dotted_fixture_subpath}"
    )



@pytest.mark.parametrize(
    "docstring",
    [
        "One line docstring description",
        """
    Multiple line docstring description.
    
    With more text.
    """,
    ],
)
def test_parse__description_only_docstring__single_markdown_section(docstring):
    sections, errors = parse_detailed(docstring)

    assert len(sections) == 1
    assert sections[0].type == Section.Type.MARKDOWN
    assert sections[0].value == dedent_strip(docstring)
    assert not errors


def test_parse__param_field__param_section():
    """Parse a simple docstring."""
    sections, errors = parse_detailed(
        f"""
        Docstring with one line param.

        :param {SOME_NAME}: {SOME_TEXT}
        """
    )
    assert len(sections) == 2
    assert sections[1].type == Section.Type.PARAMETERS
    assert_parameter_equal(
        sections[1].value[0], Parameter(SOME_NAME, annotation=empty, description=SOME_TEXT, kind=empty)
    )


@pytest.mark.parametrize(
    "param_directive_name",
    [
        "param",
        "parameter",
        "arg",
        "argument",
        "key",
        "keyword",
    ],
)
def test_parse__all_param_names__param_section(param_directive_name):
    sections, errors = parse_detailed(
        f"""
        Docstring with one line param.

        :{param_directive_name} {SOME_NAME}: {SOME_TEXT}
        """
    )
    assert len(sections) == 2
    assert sections[1].type == Section.Type.PARAMETERS
    assert_parameter_equal(
        sections[1].value[0], Parameter(SOME_NAME, annotation=empty, description=SOME_TEXT, kind=empty)
    )


@pytest.mark.parametrize(
    "docstring",
    [
        f"""
        Docstring with param with continuation, no indent.

        :param {SOME_NAME}: {SOME_TEXT}
        {SOME_EXTRA_TEXT}
        """,
        f"""
        Docstring with param with continuation, with indent.

        :param {SOME_NAME}: {SOME_TEXT}
          {SOME_EXTRA_TEXT}
        """,
    ],
)
def test_parse__param_field_multi_line__param_section(docstring):
    """Parse a simple docstring."""
    sections, errors = parse_detailed(docstring)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.PARAMETERS
    assert_parameter_equal(
        sections[1].value[0],
        Parameter(SOME_NAME, annotation=empty, description=f"{SOME_TEXT} {SOME_EXTRA_TEXT}", kind=empty),
    )


def test_parse__param_field_for_function__param_section_with_kind():
    """Parse a simple docstring."""

    def f(foo):
        """
        Docstring with line continuation.

        :param foo: descriptive test text
        """

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.PARAMETERS
    assert_parameter_equal(
        sections[1].value[0],
        Parameter(SOME_NAME, annotation=empty, description=SOME_TEXT, kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
    )


def test_parse__param_field_docs_type__param_section_with_type():
    """Parse a simple docstring."""

    def f(foo):
        """
        Docstring with line continuation.

        :param str foo: descriptive test text
        """

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.PARAMETERS
    assert_parameter_equal(
        sections[1].value[0],
        Parameter(SOME_NAME, annotation="str", description=SOME_TEXT, kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
    )


def test_parse__param_field_type_field__param_section_with_type():
    """Parse a simple docstring."""

    def f(foo):
        """
        Docstring with line continuation.

        :param foo: descriptive test text
        :type foo: str
        """

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.PARAMETERS
    assert_parameter_equal(
        sections[1].value[0],
        Parameter(SOME_NAME, annotation="str", description=SOME_TEXT, kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
    )


def test_parse__param_field_type_field_first__param_section_with_type():
    """Parse a simple docstring."""

    def f(foo):
        """
        Docstring with line continuation.

        :type foo: str
        :param foo: descriptive test text
        """

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.PARAMETERS
    assert_parameter_equal(
        sections[1].value[0],
        Parameter(SOME_NAME, annotation="str", description=SOME_TEXT, kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
    )


def test_parse__param_field_type_field_or_none__param_section_with_optional():
    """Parse a simple docstring."""

    def f(foo):
        """
        Docstring with line continuation.

        :param foo: descriptive test text
        :type foo: str or None
        """

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.PARAMETERS
    assert_parameter_equal(
        sections[1].value[0],
        Parameter(
            SOME_NAME, annotation="Optional[str]", description=SOME_TEXT, kind=inspect.Parameter.POSITIONAL_OR_KEYWORD
        ),
    )


def test_parse__param_field_type_field_or_int__param_section_with_union():
    """Parse a simple docstring."""

    def f(foo):
        """
        Docstring with line continuation.

        :param foo: descriptive test text
        :type foo: str or int
        """

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.PARAMETERS
    assert_parameter_equal(
        sections[1].value[0],
        Parameter(
            SOME_NAME, annotation="Union[str,int]", description=SOME_TEXT, kind=inspect.Parameter.POSITIONAL_OR_KEYWORD
        ),
    )


def test_parse__param_field_annotate_type__param_section_with_type():
    """Parse a simple docstring."""

    def f(foo: str):
        """
        Docstring with line continuation.

        :param foo: descriptive test text
        """

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.PARAMETERS
    assert_parameter_equal(
        sections[1].value[0],
        Parameter(SOME_NAME, annotation=str, description=SOME_TEXT, kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
    )


def test_parse__param_field_no_matching_param__result_from_docstring():
    """Parse a simple docstring."""

    def f(foo: str):
        """
        Docstring with line continuation.

        :param other: descriptive test text
        """

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.PARAMETERS
    assert_parameter_equal(
        sections[1].value[0],
        Parameter("other", annotation=empty, description=SOME_TEXT, kind=empty),
    )


def test_parse__param_field_with_default__result_from_docstring():
    """Parse a simple docstring."""

    def f(foo=""):
        """
        Docstring with line continuation.

        :param foo: descriptive test text
        """

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.PARAMETERS
    assert_parameter_equal(
        sections[1].value[0],
        Parameter(
            "foo", annotation=empty, description=SOME_TEXT, default="", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD
        ),
    )


def test_parse__param_field_no_matching_param__error_message():
    """Parse a simple docstring."""

    def f(foo: str):
        """
        Docstring with line continuation.

        :param other: descriptive test text
        """

    sections, errors = parse(f)
    assert "No matching parameter for 'other'" in errors[0]


def test_parse__invalid_param_field_only_initial_marker__error_message():
    """Parse a simple docstring."""

    def f(foo: str):
        """
        Docstring with line continuation.

        :param foo descriptive test text
        """

    sections, errors = parse(f)
    assert "Failed to get ':directive: value' pair" in errors[0]


def test_parse__invalid_param_field_wrong_part_count__error_message():
    """Parse a simple docstring."""

    def f(foo: str):
        """
        Docstring with line continuation.

        :param: descriptive test text
        """

    sections, errors = parse(f)
    assert "Failed to parse field directive" in errors[0]


def test_parse__param_twice__error_message():
    """Parse a simple docstring."""

    def f(foo: str):
        """
        Docstring with line continuation.

        :param foo: descriptive test text
        :param foo: descriptive test text again
        """

    sections, errors = parse(f)
    assert "Duplicate parameter entry for 'foo'" in errors[0]


def test_parse__param_type_twice_doc__error_message():
    """Parse a simple docstring."""

    def f(foo):
        """
        Docstring with line continuation.

        :param str foo: descriptive test text
        :type foo: str
        """

    sections, errors = parse(f)
    assert "Duplicate parameter information for 'foo'" in errors[0]


def test_parse__param_type_twice_annotated__error_message():
    """Parse a simple docstring."""

    def f(foo: str):
        """
        Docstring with line continuation.

        :param str foo: descriptive test text
        :type foo: str
        """

    sections, errors = parse(f)
    assert "Duplicate parameter information for 'foo'" in errors[0]


def test_parse__param_type_no_type__error_message():
    """Parse a simple docstring."""

    def f(foo: str):
        """
        Docstring with line continuation.

        :param str foo: descriptive test text
        :type str
        """

    sections, errors = parse(f)
    assert "Failed to get ':directive: value' pair from" in errors[0]


def test_parse__param_type_no_name__error_message():
    """Parse a simple docstring."""

    def f(foo: str):
        """
        Docstring with line continuation.

        :param str foo: descriptive test text
        :type: str
        """

    sections, errors = parse(f)
    assert "Failed to get parameter name from" in errors[0]


@pytest.mark.parametrize(
    "docstring",
    [
        f"""
        Docstring with param with continuation, no indent.

        :var {SOME_NAME}: {SOME_TEXT}
        {SOME_EXTRA_TEXT}
        """,
        f"""
        Docstring with param with continuation, with indent.

        :var {SOME_NAME}: {SOME_TEXT}
          {SOME_EXTRA_TEXT}
        """,
    ],
)
def test_parse__attribute_field_multi_line__param_section(docstring):
    """Parse a simple docstring."""
    sections, errors = parse_detailed(docstring)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.ATTRIBUTES
    assert_attribute_equal(
        sections[1].value[0],
        Attribute(SOME_NAME, annotation=empty, description=f"{SOME_TEXT} {SOME_EXTRA_TEXT}"),
    )


@pytest.mark.parametrize(
    "attribute_directive_name",
    [
        "var",
        "ivar",
        "cvar",
    ],
)
def test_parse__all_attribute_names__param_section(attribute_directive_name):
    sections, errors = parse_detailed(
        f"""
        Docstring with one line attribute.

        :{attribute_directive_name} {SOME_NAME}: {SOME_TEXT}
        """
    )
    assert len(sections) == 2
    assert sections[1].type == Section.Type.ATTRIBUTES
    assert_attribute_equal(
        sections[1].value[0],
        Attribute(SOME_NAME, annotation=empty, description=SOME_TEXT),
    )


def test_parse__class_attributes__attributes_section():
    class Foo:
        """
        Class docstring with attributes

        :var foo: descriptive test text
        """

    sections, errors = parse(Foo)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.ATTRIBUTES
    assert_attribute_equal(
        sections[1].value[0],
        Attribute(SOME_NAME, annotation=empty, description=SOME_TEXT),
    )


def test_parse__return_directive__return_section_no_type():
    def f(foo: str):
        """
        Function with only return directive

        :return: descriptive test text
        """
        return foo

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.RETURN
    assert_annotated_obj_equal(
        sections[1].value,
        AnnotatedObject(annotation=empty, description=SOME_TEXT),
    )


def test_parse__return_directive_rtype__return_section_with_type():
    def f(foo: str):
        """
        Function with only return & rtype directive

        :return: descriptive test text
        :rtype: str
        """
        return foo

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.RETURN
    assert_annotated_obj_equal(
        sections[1].value,
        AnnotatedObject(annotation="str", description=SOME_TEXT),
    )


def test_parse__return_directive_annotation__return_section_with_type():
    def f(foo: str) -> str:
        """
        Function with return directive, rtype directive, & annotation

        :return: descriptive test text
        """
        return foo

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.RETURN
    assert_annotated_obj_equal(
        sections[1].value,
        AnnotatedObject(annotation=str, description=SOME_TEXT),
    )


def test_parse__return_directive_annotation__return_section_with_type_error():
    def f(foo: str) -> str:
        """
        Function with return directive, rtype directive, & annotation

        :return: descriptive test text
        :rtype: str
        """
        return foo

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.RETURN
    assert_annotated_obj_equal(
        sections[1].value,
        AnnotatedObject(annotation=str, description=SOME_TEXT),
    )
    assert "Duplicate type information for return" in errors[0]


def test_parse__raises_directive__exception_section():
    def f(foo: str):
        """
        Function with only return directive

        :raise SomeException: descriptive test text
        """
        return foo

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.EXCEPTIONS
    assert_annotated_obj_equal(
        sections[1].value[0],
        AnnotatedObject(annotation=SOME_EXCEPTION_NAME, description=SOME_TEXT),
    )


def test_parse__multiple_raises_directive__exception_section_with_two():
    def f(foo: str):
        """
        Function with only return directive

        :raise SomeException: descriptive test text
        :raise SomeOtherException: descriptive test text
        """
        return foo

    sections, errors = parse(f)
    assert len(sections) == 2
    assert sections[1].type == Section.Type.EXCEPTIONS
    assert_annotated_obj_equal(
        sections[1].value[0],
        AnnotatedObject(annotation=SOME_EXCEPTION_NAME, description=SOME_TEXT),
    )
    assert_annotated_obj_equal(
        sections[1].value[1],
        AnnotatedObject(annotation=SOME_OTHER_EXCEPTION_NAME, description=SOME_TEXT),
    )


@pytest.mark.parametrize(
    "attribute_directive_name",
    [
        "raises",
        "raise",
        "except",
        "exception",
    ],
)
def test_parse__all_exception_names__param_section(attribute_directive_name):
    sections, errors = parse_detailed(
        f"""
        Docstring with one line attribute.

        :{attribute_directive_name} {SOME_EXCEPTION_NAME}: {SOME_TEXT}
        """
    )
    assert len(sections) == 2
    assert sections[1].type == Section.Type.EXCEPTIONS
    assert_annotated_obj_equal(
        sections[1].value[0],
        AnnotatedObject(annotation=SOME_EXCEPTION_NAME, description=SOME_TEXT),
    )


# -------------------------------
# Fixture tests
# -------------------------------


def test_parse_module_attributes_section__expected_attributes_section():
    """Parse attributes section in modules."""
    obj = get_rst_object_documentation("docstring_attributes_section")
    assert len(obj.docstring_sections) == 2
    attr_section = obj.docstring_sections[1]
    assert attr_section.type == Section.Type.ATTRIBUTES
    assert len(attr_section.value) == 5
    expected = [
        {"name": "A", "annotation": "int", "description": "Alpha."},
        # type annotation takes preference over docstring
        {"name": "B", "annotation": "str", "description": "Beta."},
        {"name": "C", "annotation": "bool", "description": "Gamma."},
        {"name": "D", "annotation": "", "description": "Delta."},
        {"name": "E", "annotation": "float", "description": "Epsilon."},
    ]
    assert [serialize_attribute(attr) for attr in attr_section.value] == expected


def test_parse_module_attributes_section__expected_docstring_errors():
    """Parse attributes section in modules."""
    obj = get_rst_object_documentation("docstring_attributes_section")
    assert len(obj.docstring_errors) == 1
    assert "Duplicate attribute information for 'B'" in obj.docstring_errors[0]


def test_property_docstring():
    """Parse a property docstring."""
    class_ = get_rst_object_documentation("docstrings.NotDefinedYet")
    prop = class_.attributes[0]
    sections, errors = prop.docstring_sections, prop.docstring_errors
    assert len(sections) == 2
    assert not errors
