"""Tests for [the `objects` module][pytkdocs.objects]."""
import os

from pytkdocs.loader import Loader
from pytkdocs.objects import Attribute, Class, Function, Method, Module, Object
from tests import FIXTURES_DIR


def test_creating_module():
    """Create a Module."""
    assert Module(name="my_object", path="my.dotted.path", file_path="/my/absolute/path.py")


def test_creating_class():
    """Create a Class."""
    assert Class(name="my_object", path="my.dotted.path", file_path="/my/absolute/path.py")


def test_creating_method():
    """Create a Method."""
    assert Method(name="my_object", path="my.dotted.path", file_path="/my/absolute/path.py")


def test_creating_function():
    """Create a Function."""
    assert Function(name="my_object", path="my.dotted.path", file_path="/my/absolute/path.py")


def test_creating_attribute():
    """Create an Attribute."""
    assert Attribute(name="my_object", path="my.dotted.path", file_path="/my/absolute/path.py")


def test_add_child():
    """Add a child."""
    parent = Module(name="my_module", path="my.dotted.path", file_path="/my/absolute/path.py")
    child = Attribute(name="my_attribute", path="my.dotted.path.my_attribute", file_path="/my/absolute/path.py")
    parent.add_child(child)
    assert parent.children[0] is child
    assert parent.attributes[0] is child


def test_do_not_add_child_if_parent_is_not_self():
    """Don't add a child the parent is not the right one."""
    parent = Module(name="my_module", path="my.dotted.path", file_path="/my/absolute/path.py")
    child = Attribute(name="my_attribute", path="my.other.path.my_attribute", file_path="/my/absolute/path.py")
    parent.add_child(child)
    assert not parent.children
    assert not parent.attributes


def test_get_root():
    """Get the root object."""
    root = Module(name="my_module", path="my.dotted.path", file_path="")
    node1 = Class(name="my_class1", path="my.dotted.path.my_class1", file_path="")
    node2 = Class(name="my_class2", path="my.dotted.path.my_class2", file_path="")
    leaf = Method(name="my_method", path="my.dotted.path.my_class1.my_method", file_path="")

    root.add_children([node1, node2])
    node1.add_child(leaf)

    assert root.root is root
    assert node1.root is root
    assert node2.root is root
    assert leaf.root is root


def test_relative_file_path_for_root():
    """Get the relative file of a shallow object."""
    obj = Object(
        name="nested_class", path="tests.fixtures.nested_class", file_path=str(FIXTURES_DIR / "nested_class.py")
    )
    assert obj.relative_file_path == os.path.join("tests", "fixtures", "nested_class.py")


def test_relative_file_path_for_leaf():
    """Get the relative file path of a deep object."""
    obj = Loader().get_object_documentation("tests.fixtures.pkg1")
    leaf = obj.children[0].children[0].children[0].children[0]
    assert leaf.relative_file_path == os.path.join(
        "tests", "fixtures", "pkg1", "pkg2", "pkg3", "pkg4", "pkg5", "__init__.py"
    )


def test_no_relative_file_path_for_non_existent_package():
    """Cannot find relative file path."""
    obj = Object(name="o", path="a.b.o", file_path="/some/non_existent/path/a/b/o.py")
    assert not obj.relative_file_path


def test_no_relative_file_path_for_wrong_path():
    """Cannot find relative file path with wrong dotted path."""
    obj = Object(name="o", path="wrong.dotted.path", file_path=str(FIXTURES_DIR / "nested_class.py"))
    assert not obj.relative_file_path


def test_no_relative_file_path_for_wrong_file_path():
    """Cannot find relative file path with wrong file path."""
    obj = Object(name="o", path="tests.fixtures.nested_class", file_path="/wrong/module/path.py")
    assert not obj.relative_file_path


def test_add_children():
    """Add multiple children at once."""
    root = Object(name="o", path="o", file_path="o.py")

    class_ = Class(name="c", path="o.c", file_path="o.py")
    attribute = Attribute(name="a", path="o.c.a", file_path="o.py")
    class_.add_child(attribute)

    root.add_children(
        [
            # class has wrong path
            Class(name="w", path="wrong.path.w", file_path="/wrong/path/w.py"),
            # class OK
            class_,
            # not a direct child,
            attribute,
            # function OK
            Function(name="f", path="o.f", file_path="o.py"),
            # not a direct child, not even a child of known child
            Method(name="missing_node", path="o.mn.missing_node", file_path="o.py"),
        ]
    )

    assert len(root.children) == 2
    assert root.classes and root.classes[0] is class_
    assert root.functions and root.functions[0].name == "f"


def test_has_contents():
    """Check if an object has contents."""
    obj = Loader().get_object_documentation("tests.fixtures.pkg1")
    assert obj.has_contents()

    obj = Loader().get_object_documentation("tests.fixtures.__init__")
    assert not obj.children
    assert obj.has_contents()  # we specified that the root always 'has contents'

    obj = Loader().get_object_documentation("tests.fixtures.no_contents")
    assert obj.children
    assert obj.has_contents
    assert not obj.children[0].has_contents()


def test_has_no_contents():
    """Check that an object has no contents."""
    pass  # TODO
