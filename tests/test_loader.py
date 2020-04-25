"""Tests for [the `loader` module][pytkdocs.loader]."""

import sys
from pathlib import Path

import pytest

from pytkdocs.loader import Loader, get_object_tree

from . import FIXTURES_DIR


def test_import_no_path():
    with pytest.raises(ValueError):
        get_object_tree("")


def test_import_error():
    with pytest.raises(ImportError):
        get_object_tree("eeeeeeeeeeeeeeeeeee")


def test_can_find_class_real_path():
    leaf = get_object_tree("tests.fixtures.real_path.module_a.DefinedInModuleB")
    assert leaf.dotted_path == "tests.fixtures.real_path.module_b.DefinedInModuleB"


def test_can_find_class_method_real_path():
    leaf = get_object_tree("tests.fixtures.real_path.module_a.DefinedInModuleB.method")
    assert leaf.dotted_path == "tests.fixtures.real_path.module_b.DefinedInModuleB.method"


def test_can_find_class_attribute_real_path():
    leaf = get_object_tree("tests.fixtures.real_path.module_a.DefinedInModuleB.ATTRIBUTE")
    assert leaf.dotted_path == "tests.fixtures.real_path.module_b.DefinedInModuleB.ATTRIBUTE"


def test_cannot_find_module_attribute_real_path():
    leaf = get_object_tree("tests.fixtures.real_path.module_a.ATTRIBUTE")
    assert not leaf.dotted_path == "tests.fixtures.real_path.module_b.ATTRIBUTE"


def test_inheriting_enum_Enum():
    """See  details at [tests.fixtures.inheriting_enum_Enum][]."""
    loader = Loader()
    loader.get_object_documentation("tests.fixtures.inheriting_enum_Enum")
    assert not loader.errors


def test_inheriting_typing_NamedTuple():
    """See  details at [tests.fixtures.inheriting_typing_NamedTuple][]."""
    loader = Loader()
    loader.get_object_documentation("tests.fixtures.inheriting_typing_NamedTuple")

    if sys.version.startswith("3.8"):
        assert len(loader.errors) == 1
    else:
        # there are 4 class-attributes, 2 errors (source, signature) per attribute
        assert len(loader.errors) >= 8
        for error in loader.errors[-8:]:
            assert "itemgetter" in error
        for error in loader.errors[:-8]:
            assert "could not get source code" in error


def test_nested_class():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.nested_class")
    assert obj.classes
    assert obj.classes[0].docstring == "Main docstring."
    assert obj.classes[0].classes
    assert obj.classes[0].classes[0].docstring == "Nested docstring."


def test_loading_deep_package():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.pkg1.pkg2.pkg3.pkg4.pkg5")
    assert obj.docstring == "Hello from the abyss."
    assert obj.path == "tests.fixtures.pkg1.pkg2.pkg3.pkg4.pkg5"


def test_loading_package():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package")
    assert obj.docstring == "The package docstring."


def test_loading_namespace_package():
    loader = Loader()
    old_paths = list(sys.path)
    sys.path.append(str(Path(FIXTURES_DIR).resolve()))
    obj = loader.get_object_documentation("test_namespace.subspace")
    assert obj.docstring == "The subspace package docstring."
    assert obj.relative_file_path == "subspace/__init__.py"
    sys.path = old_paths


def test_loading_module():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module")
    assert obj.docstring == "The module docstring."


def test_loading_class():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module.TheClass")
    assert obj.docstring == "The class docstring."


def test_loading_nested_class():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module.TheClass.TheNestedClass")
    assert obj.docstring == "The nested class docstring."


def test_loading_double_nested_class():
    loader = Loader()
    obj = loader.get_object_documentation(
        "tests.fixtures.the_package.the_module.TheClass.TheNestedClass.TheDoubleNestedClass"
    )
    assert obj.docstring == "The double nested class docstring."


def test_loading_class_attribute():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module.TheClass.THE_ATTRIBUTE")
    assert obj.docstring == "The attribute 0.1 docstring."


def test_loading_nested_class_attribute():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module.TheClass.TheNestedClass.THE_ATTRIBUTE")
    assert obj.docstring == "The attribute 0.2 docstring."


def test_loading_double_nested_class_attribute():
    loader = Loader()
    obj = loader.get_object_documentation(
        "tests.fixtures.the_package.the_module.TheClass.TheNestedClass.TheDoubleNestedClass.THE_ATTRIBUTE"
    )
    assert obj.docstring == "The attribute 0.3 docstring."


def test_loading_class_method():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module.TheClass.the_method")
    assert obj.docstring == "The method1 docstring."


def test_loading_nested_class_method():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module.TheClass.TheNestedClass.the_method")
    assert obj.docstring == "The method2 docstring."


def test_loading_double_nested_class_method():
    loader = Loader()
    obj = loader.get_object_documentation(
        "tests.fixtures.the_package.the_module.TheClass.TheNestedClass.TheDoubleNestedClass.the_method"
    )
    assert obj.docstring == "The method3 docstring."


def test_loading_staticmethod():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module.TheClass.the_static_method")
    assert obj.docstring == "The static method docstring."


def test_loading_classmethod():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module.TheClass.the_class_method")
    assert obj.docstring == "The class method docstring."


def test_loading_property():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module.TheClass.the_property")
    assert obj.docstring == "The property docstring."


def test_loading_writable_property():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module.TheClass.the_writable_property")
    assert obj.docstring == "The writable property getter docstring."


def test_loading_function():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module.the_function")
    assert obj.docstring == "The function docstring."


def test_loading_attribute():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module.THE_ATTRIBUTE")
    assert obj.docstring == "The attribute docstring."


def test_loading_explicit_members():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module", members={"TheClass"})
    assert len(obj.children) == 1
    assert obj.children[0].name == "TheClass"


def test_loading_no_members():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module", members=False)
    assert not obj.children


def test_loading_with_filters():
    loader = Loader(filters=["!^[A-Z_]+$"])
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module")
    for child in obj.children:
        assert child.name != "THE_ATTRIBUTE"


def test_loading_with_filters_reselection():
    loader = Loader(filters=["![A-Z_]", "[a-z]"])
    obj = loader.get_object_documentation("tests.fixtures.the_package.the_module")
    assert obj.classes
    assert obj.classes[0].name == "TheClass"


def test_loading_with_members_and_filters():
    loader = Loader(filters=["!THE"])
    obj = loader.get_object_documentation(
        "tests.fixtures.the_package.the_module", members={"THE_ATTRIBUTE", "TheClass"}
    )
    assert obj.attributes
    assert obj.attributes[0].name == "THE_ATTRIBUTE"
    assert obj.classes
    assert obj.classes[0].name == "TheClass"
    assert not any(a.name == "THE_ATTRIBUTE" for a in obj.classes[0].attributes)


def test_loading_members_set_at_import_time():
    loader = Loader()
    obj = loader.get_object_documentation("tests.fixtures.dynamic_members")
    assert obj.functions
    assert len(obj.classes) == 1
    class_ = obj.classes[0]
    assert class_.methods
