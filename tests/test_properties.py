"""Tests for [the `properties` module][pytkdocs.properties]."""

from pytkdocs.objects import Attribute, Class, Function, Method, Module


def test_name_properties_on_module():
    """Check module name properties."""
    assert not Module(name="a", path="a", file_path="a.py").name_properties
    assert "private" in Module(name="_a", path="a", file_path="_a.py").name_properties
    assert not Module(name="__a", path="__a", file_path="__a.py").name_properties
    assert "special" in Module(name="__a__", path="a", file_path="__a__.py").name_properties


def test_name_properties_on_class():
    """Check class name properties."""
    assert not Class(name="b", path="a.b", file_path="a.py").name_properties
    assert "private" in Class(name="_b", path="a._b", file_path="a.py").name_properties
    assert not Class(name="__b", path="a.__b", file_path="a.py").name_properties
    assert not Class(name="__b__", path="a.__b__", file_path="a.py").name_properties


def test_name_properties_on_method():
    """Check method name properties."""
    assert not Method(name="c", path="a.b.c", file_path="a.py").name_properties
    assert "private" in Method(name="_c", path="a.b._c", file_path="a.py").name_properties
    assert not Method(name="__c", path="a.b.__c", file_path="a.py").name_properties
    assert "special" in Method(name="__c__", path="a.b.__c__", file_path="a.py").name_properties


def test_name_properties_on_function():
    """Check function name properties."""
    assert not Function(name="b", path="a.b", file_path="a.py").name_properties
    assert "private" in Function(name="_b", path="a._b", file_path="a.py").name_properties
    assert not Function(name="__b", path="a.__b", file_path="a.py").name_properties
    assert not Function(name="__b__", path="a.__b__", file_path="a.py").name_properties


def test_name_properties_on_attribute():
    """Check attribute name properties."""
    assert not Attribute(name="b", path="a.b", file_path="a.py").name_properties
    assert "private" in Attribute(name="_b", path="a._b", file_path="a.py").name_properties
    assert "class-private" in Attribute(name="__b", path="a.__b", file_path="a.py").name_properties
    assert "special" in Attribute(name="__b__", path="a.__b__", file_path="a.py").name_properties
