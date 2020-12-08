"""Tests for [the `parsers.attributes` module][pytkdocs.parsers.attributes] on annotations."""


from tests.fixtures.parsing import annotations

from pytkdocs.parsers.attributes import get_instance_attributes


class TestAnnotations:
    def setup(self):
        """Setup reusable attributes."""
        self.attributes = get_instance_attributes(annotations.C.__init__)

    def test_parse_dict_annotation(self):
        assert "dict_annotation" in self.attributes
        assert self.attributes["dict_annotation"]["annotation"] == "Dict[str, Any]"

    def test_parse_list_annotation(self):
        assert "list_annotation" in self.attributes
        assert self.attributes["list_annotation"]["annotation"] == "List[str]"
