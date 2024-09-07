"""Tests for [the `parsers.attributes` module][pytkdocs.parsers.attributes]."""

from pytkdocs.parsers.attributes import get_class_attributes, get_instance_attributes, get_module_attributes
from tests.fixtures.parsing import attributes as attr_module


class TestParsing:
    """Test the parser in general."""

    attributes = get_module_attributes(attr_module)

    def test_parse_tuple_target(self) -> None:
        """Assert can parse `a, b, c = 0, 0, 0`."""
        assert "OK" in self.attributes
        assert "WARNING" in self.attributes
        assert "CRITICAL" in self.attributes
        assert "UNKNOWN" in self.attributes


class TestModuleAttributes:
    """Test the parser for module attributes."""

    attributes = get_module_attributes(attr_module)

    def test_pick_up_attribute_without_docstring(self) -> None:
        """Don't pick attributes without docstrings."""
        assert "NO_DOC_NO_TYPE" in self.attributes
        assert "NO_DOC_NO_VALUE" in self.attributes
        assert "NO_DOC" in self.attributes

    def test_pick_up_attribute_without_type(self) -> None:
        """Pick up attribute without a type."""
        assert "NO_TYPE" in self.attributes
        assert self.attributes["NO_TYPE"]["docstring"] == "No type."

    def test_pick_up_attribute_without_value(self) -> None:
        """Pick up attribute without a value."""
        assert "NO_VALUE" in self.attributes
        assert self.attributes["NO_VALUE"]["docstring"] == "No value."

    def test_pick_up_attribute_with_type_and_value(self) -> None:
        """Pick up attribute with type and value."""
        assert "FULL" in self.attributes
        assert self.attributes["FULL"]["docstring"] == "Full."

    def test_pick_up_attribute_with_complex_type(self) -> None:
        """Pick up attribute with complex type."""
        assert "COMPLEX_TYPE" in self.attributes
        assert self.attributes["COMPLEX_TYPE"]["docstring"] == "Complex type."

    def test_pick_up_attribute_in_if(self) -> None:
        """Pick attribute in `if` and `else`."""
        assert "IN_IF" in self.attributes
        assert self.attributes["IN_IF"]["docstring"] == "In if."

        assert "IN_ELSE" in self.attributes
        assert self.attributes["IN_ELSE"]["docstring"] == "In else."

    def test_pick_up_attribute_in_try_except(self) -> None:
        """Pick attribute in `try`, `except`, `else` and `finally`.."""
        assert "IN_TRY" in self.attributes
        assert self.attributes["IN_TRY"]["docstring"] == "In try."

        assert "IN_EXCEPT" in self.attributes
        assert self.attributes["IN_EXCEPT"]["docstring"] == "In except."

        assert "IN_TRY_ELSE" in self.attributes
        assert self.attributes["IN_TRY_ELSE"]["docstring"] == "In try else."

        assert "IN_FINALLY" in self.attributes
        assert self.attributes["IN_FINALLY"]["docstring"] == "In finally."

    def test_docstring_is_correctly_dedented(self) -> None:  # noqa: D102
        assert "\n    " not in self.attributes["DEDENT"]["docstring"]


class TestClassAttributes:
    """Test the parser for module attributes."""

    attributes = get_class_attributes(attr_module.E)

    def test_pick_up_attribute_in_class(self) -> None:
        """Pick up class attribute."""
        assert "IN_CLASS" in self.attributes
        assert self.attributes["IN_CLASS"]["docstring"] == "In class."

    def test_docstring_is_correctly_dedented(self) -> None:  # noqa: D102
        assert "\n    " not in self.attributes["DEDENT"]["docstring"]


class TestInstanceAttributes:
    """Test the parser for module attributes."""

    attributes = get_instance_attributes(attr_module.E.__init__)

    def test_pick_up_attribute_in_init_method(self) -> None:
        """Pick up instance attribute."""
        assert "in_init" in self.attributes
        assert self.attributes["in_init"]["docstring"] == "In init."

    def test_do_not_pick_up_non_attributes(self) -> None:
        """Don't pick documented variables in functions."""
        assert "non_attribute" not in self.attributes
        assert "non_attribute2" not in self.attributes
        assert "non_self_attribute" not in self.attributes
        assert "non_self_attribute2" not in self.attributes

    def test_do_not_pick_up_subscript_attribute(self) -> None:
        """Don't pick documented variables in functions."""
        assert "d" not in self.attributes
        assert "d.subscript" not in self.attributes
        assert "subscript" not in self.attributes

    def test_docstring_is_correctly_dedented(self) -> None:  # noqa: D102
        assert "\n    " not in self.attributes["dedent"]["docstring"]


class TestPydanticFields:
    """Test the parser for module attributes."""

    attributes = get_class_attributes(attr_module.Model)

    def test_pick_up_attribute_in_pydantic_model(self) -> None:
        """Pick up attribute in Pydantic model."""
        assert "in_pydantic_model" in self.attributes
        assert self.attributes["in_pydantic_model"]["docstring"] == "In Pydantic model."

        assert "model_field" in self.attributes
        assert self.attributes["model_field"]["docstring"] == "A model field."


class TestMarshmallowFields:
    """Test the parser for module attributes."""

    attributes = get_class_attributes(attr_module.MarshmallowSchema)

    def test_pick_up_attribute_in_pydantic_model(self) -> None:
        """Pick up attribute in Marshmallow model."""
        assert "in_marshmallow_model" in self.attributes
        assert self.attributes["in_marshmallow_model"]["docstring"] == "In Marshmallow model."

        assert "model_field" in self.attributes
        assert self.attributes["model_field"]["docstring"] == "A model field."
