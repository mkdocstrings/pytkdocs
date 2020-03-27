"""
This module is responsible for loading the documentation from Python objects.

It uses [`inspect`](https://docs.python.org/3/library/inspect.html) for introspecting objects,
iterating over their members, etc.
"""

import importlib
import inspect
import pkgutil
import re
import textwrap
from functools import lru_cache
from pathlib import Path
from typing import Any, List, Optional, Set, Union

from .objects import Attribute, Class, Function, Method, Module, Object, Source
from .parsers.attributes import get_attributes
from .properties import RE_SPECIAL


class ObjectNode:
    """
    Helper class to represent an object tree.

    It's not really a tree but more a backward-linked list:
    each node has a reference to its parent, but not to its child (for simplicity purposes and to avoid bugs).

    Each node stores an object, its name, and a reference to its parent node.
    """

    def __init__(self, obj: Any, name: str, parent: Optional["ObjectNode"] = None) -> None:
        self.obj: Any = obj
        """The actual Python object."""

        self.name: str = name
        """The Python object's name."""

        self.parent: Optional[ObjectNode] = parent
        """The parent node."""

    @property
    def dotted_path(self) -> str:
        """The Python dotted path of the object."""
        parts = [self.name]
        current = self.parent
        while current:
            parts.append(current.name)
            current = current.parent
        return ".".join(reversed(parts))

    @property
    def file_path(self) -> str:
        """The object's module file path."""
        return inspect.getabsfile(self.root.obj)

    @property
    def root(self) -> "ObjectNode":
        """The root of the tree."""
        if self.parent is not None:
            return self.parent.root
        return self

    def is_module(self) -> bool:
        """Is this node's object a module?"""
        return inspect.ismodule(self.obj)

    def is_class(self) -> bool:
        """Is this node's object a class?"""
        return inspect.isclass(self.obj)

    def is_function(self) -> bool:
        """Is this node's object a function?"""
        return inspect.isfunction(self.obj)

    def is_property(self) -> bool:
        """Is this node's object a property?"""
        return isinstance(self.obj, property)

    def parent_is_class(self) -> bool:
        """Is the object of this node's parent a class?"""
        return bool(self.parent and self.parent.is_class())

    def is_method(self) -> bool:
        """Is this node's object a method?"""
        return self.parent_is_class() and isinstance(self.obj, type(lambda: 0))

    def is_staticmethod(self) -> bool:
        """Is this node's object a staticmethod?"""
        if not self.parent:
            return False
        return self.parent_is_class() and isinstance(self.parent.obj.__dict__.get(self.name, None), staticmethod)

    def is_classmethod(self) -> bool:
        """Is this node's object a classmethod?"""
        if not self.parent:
            return False
        return self.parent_is_class() and isinstance(self.parent.obj.__dict__.get(self.name, None), classmethod)


def get_object_tree(path: str) -> ObjectNode:
    """
    Transform a path into an actual Python object.

    The path can be arbitrary long. You can pass the path to a package,
    a module, a class, a function or a global variable, as deep as you
    want, as long as the deepest module is importable through
    `importlib.import_module` and each object is obtainable through
    the `getattr` method. It is not possible to load local objects.

    Args:
        path: the dot-separated path of the object.

    Raises:
        ValueError: when the path is not valid (evaluates to `False`).
        ImportError: when the object or its parent module could not be imported.

    Returns:
        The leaf node representing the object and its parents.
    """
    if not path:
        raise ValueError(f"path must be a valid Python path, not {path}")

    # We will try to import the longest dotted-path first.
    # If it fails, we remove the right-most part and put it in a list of "objects", used later.
    # We loop until we find the deepest importable submodule.
    obj_parent_modules = path.split(".")
    objects: List[str] = []

    while True:
        parent_module_path = ".".join(obj_parent_modules)
        try:
            parent_module = importlib.import_module(parent_module_path)
        except ImportError:
            if len(obj_parent_modules) == 1:
                raise ImportError("No module named '%s'" % obj_parent_modules[0])
            objects.insert(0, obj_parent_modules.pop(-1))
        else:
            break

    # We now have the module containing the desired object.
    # We will build the object tree by iterating over the previously stored objects names
    # and trying to get them as attributes.
    current_node = ObjectNode(parent_module, parent_module.__name__)
    for obj_name in objects:
        obj = getattr(current_node.obj, obj_name)
        current_node.child = ObjectNode(obj, obj_name, parent=current_node)  # type: ignore
        current_node = current_node.child  # type: ignore

    leaf = current_node

    # We now try to get the "real" parent module, not the one the object was imported into.
    # This is important if we want to be able to retrieve the docstring of an attribute for example.
    # Once we find an object for which we could get the module, we stop trying to get the module.
    # Once we reach the node before the root, we apply the module if found, and break.
    real_module = None
    while current_node.parent is not None:
        if real_module is None:
            real_module = inspect.getmodule(current_node.obj)
        if inspect.ismodule(current_node.parent.obj):
            if real_module is not None and real_module is not current_node.parent.obj:
                current_node.parent = ObjectNode(real_module, real_module.__name__)
            break
        current_node = current_node.parent

    return leaf


class Loader:
    """
    This class contains the object documentation loading mechanisms.

    Any error that occurred during collection of the objects and their documentation is stored in the `errors` list.
    """

    def __init__(self, filters: Optional[List[str]] = None):
        """
        Arguments:
            filters: A list of regular expressions to fine-grain select members. It is applied recursively.
        """
        if not filters:
            filters = []

        self.filters = [(f, re.compile(f.lstrip("!"))) for f in filters]
        self.errors: List[str] = []

    def get_object_documentation(self, dotted_path: str, members: Optional[Union[Set[str], bool]] = None) -> Object:
        """
        Get the documentation for an object and its children.

        Arguments:
            dotted_path: The Python dotted path to the desired object.
            members: `True` to select members and filter them, `False` to select no members,
                or a list of names to explicitly select the members with these names.
                It is applied only on the root object.

        Return:
            The documented object.
        """

        if members is True:
            members = set()

        root_object: Object
        leaf = get_object_tree(dotted_path)

        attributes = get_attributes(leaf.root.obj)

        if leaf.is_module():
            root_object = self.get_module_documentation(leaf, members)
        elif leaf.is_class():
            root_object = self.get_class_documentation(leaf, members)
        elif leaf.is_staticmethod():
            root_object = self.get_staticmethod_documentation(leaf)
        elif leaf.is_classmethod():
            root_object = self.get_classmethod_documentation(leaf)
        elif leaf.is_method():
            root_object = self.get_regular_method_documentation(leaf)
        elif leaf.is_function():
            root_object = self.get_function_documentation(leaf)
        elif leaf.is_property():
            root_object = self.get_property_documentation(leaf)
        else:
            for attribute in attributes:
                if attribute.path == dotted_path:
                    return attribute
            raise ValueError(f"{dotted_path}: {type(leaf.obj)} not yet supported")

        if members is not False:
            filtered = []
            for attribute in attributes:
                if attribute.parent_path == root_object.path:
                    if self.select(attribute.name, members):  # type: ignore
                        filtered.append(attribute)
                elif self.select(attribute.name, set()):
                    filtered.append(attribute)
            root_object.dispatch_attributes(filtered)

        root_object.parse_all_docstring()

        return root_object

    def get_module_documentation(self, node: ObjectNode, members=None) -> Module:
        """
        Get the documentation for a module and its children.

        Arguments:
            node: The node representing the module and its parents.
            members: Explicit members to select.

        Return:
            The documented module object.
        """
        module = node.obj
        path = node.dotted_path
        name = path.split(".")[-1]
        source: Optional[Source]

        try:
            source = Source(inspect.getsource(module), 1)
        except OSError as error:
            try:
                with Path(node.file_path).open() as fd:
                    contents = fd.readlines()
                    if contents:
                        source = Source(contents, 1)
                    else:
                        source = None
            except OSError:
                self.errors.append(f"Couldn't read source for '{path}': {error}")
                source = None

        root_object = Module(
            name=name, path=path, file_path=node.file_path, docstring=inspect.getdoc(module) or "", source=source,
        )

        if members is False:
            return root_object

        members = members or set()

        for member_name, member in inspect.getmembers(module):
            if self.select(member_name, members):  # type: ignore
                child_node = ObjectNode(member, member_name, parent=node)
                if child_node.is_class() and child_node.root.obj is inspect.getmodule(member):
                    root_object.add_child(self.get_class_documentation(child_node))
                elif child_node.is_function() and child_node.root.obj is inspect.getmodule(member):
                    root_object.add_child(self.get_function_documentation(child_node))

        try:
            package_path = module.__path__
        except AttributeError:
            pass
        else:
            for _, modname, _ in pkgutil.iter_modules(package_path):
                if self.select(modname, members):
                    leaf = get_object_tree(f"{path}.{modname}")
                    root_object.add_child(self.get_module_documentation(leaf))

        return root_object

    def get_class_documentation(self, node: ObjectNode, members=None) -> Class:
        """
        Get the documentation for a class and its children.

        Arguments:
            node: The node representing the class and its parents.
            members: Explicit members to select.

        Return:
            The documented class object.
        """
        class_ = node.obj
        docstring = textwrap.dedent(class_.__doc__ or "")
        root_object = Class(name=node.name, path=node.dotted_path, file_path=node.file_path, docstring=docstring)

        if members is False:
            return root_object

        members = members or set()

        for member_name, member in class_.__dict__.items():
            if member is type or member is object:
                continue

            if not self.select(member_name, members):  # type: ignore
                continue

            child_node = ObjectNode(getattr(class_, member_name), member_name, parent=node)
            if child_node.is_class():
                root_object.add_child(self.get_class_documentation(child_node))
            elif child_node.is_classmethod():
                root_object.add_child(self.get_classmethod_documentation(child_node))
            elif child_node.is_staticmethod():
                root_object.add_child(self.get_staticmethod_documentation(child_node))
            elif child_node.is_method():
                root_object.add_child(self.get_regular_method_documentation(child_node))
            elif child_node.is_property():
                root_object.add_child(self.get_property_documentation(child_node))

        return root_object

    def get_function_documentation(self, node: ObjectNode) -> Function:
        """
        Get the documentation for a function.

        Arguments:
            node: The node representing the function and its parents.

        Return:
            The documented function object.
        """
        function = node.obj
        path = node.dotted_path
        source: Optional[Source]
        signature: Optional[inspect.Signature]

        try:
            signature = inspect.signature(function)
        except TypeError as error:
            self.errors.append(f"Couldn't get signature for '{path}': {error}")
            signature = None

        try:
            source = Source(*inspect.getsourcelines(function))
        except OSError as error:
            self.errors.append(f"Couldn't read source for '{path}': {error}")
            source = None

        return Function(
            name=node.name,
            path=node.dotted_path,
            file_path=node.file_path,
            docstring=inspect.getdoc(function),
            signature=signature,
            source=source,
        )

    def get_property_documentation(self, node: ObjectNode) -> Attribute:
        """
        Get the documentation for an attribute.

        Arguments:
            node: The node representing the attribute and its parents.

        Return:
            The documented attribute object.
        """
        prop = node.obj
        path = node.dotted_path
        properties = ["property", "readonly" if prop.fset is None else "writable"]
        source: Optional[Source]

        try:
            signature = inspect.signature(prop.fget)
        except (TypeError, ValueError) as error:
            self.errors.append(f"Couldn't get signature for '{path}': {error}")
            attr_type = None
        else:
            attr_type = signature.return_annotation

        try:
            source = Source(*inspect.getsourcelines(prop.fget))
        except (OSError, TypeError) as error:
            self.errors.append(f"Couldn't get source for '{path}': {error}")
            source = None

        return Attribute(
            name=node.name,
            path=path,
            file_path=node.file_path,
            docstring=inspect.getdoc(prop.fget),
            attr_type=attr_type,
            properties=properties,
            source=source,
        )

    def get_classmethod_documentation(self, node: ObjectNode) -> Method:
        """
        Get the documentation for a class-method.

        Arguments:
            node: The node representing the class-method and its parents.

        Return:
            The documented method object.
        """
        return self.get_method_documentation(node, ["classmethod"])

    def get_staticmethod_documentation(self, node: ObjectNode) -> Method:
        """
        Get the documentation for a static-method.

        Arguments:
            node: The node representing the static-method and its parents.

        Return:
            The documented method object.
        """
        return self.get_method_documentation(node, ["staticmethod"])

    def get_regular_method_documentation(self, node: ObjectNode) -> Method:
        """
        Get the documentation for a regular method (not class- nor static-method).

        We do extra processing in this method to discard docstrings of `__init__` methods
        that were inherited from parent classes.

        Arguments:
            node: The node representing the method and its parents.

        Return:
            The documented method object.
        """
        method = self.get_method_documentation(node)
        if node.parent:
            class_ = node.parent.obj
            if RE_SPECIAL.match(node.name):
                docstring = method.docstring
                parent_classes = class_.__mro__[1:]
                for parent_class in parent_classes:
                    try:
                        parent_method = getattr(parent_class, node.name)
                    except AttributeError:
                        continue
                    else:
                        if docstring == inspect.getdoc(parent_method):
                            method.docstring = ""
                        break
        return method

    def get_method_documentation(self, node: ObjectNode, properties: Optional[List[str]] = None) -> Method:
        """
        Get the documentation for a method.

        Arguments:
            node: The node representing the method and its parents.
            properties: A list of properties to apply to the method.

        Return:
            The documented method object.
        """
        method = node.obj
        path = node.dotted_path
        source: Optional[Source]

        try:
            source = Source(*inspect.getsourcelines(method))
        except OSError as error:
            self.errors.append(f"Couldn't read source for '{path}': {error}")
            source = None
        except TypeError:
            source = None

        return Method(
            name=node.name,
            path=path,
            file_path=node.file_path,
            docstring=inspect.getdoc(method),
            signature=inspect.signature(method),
            properties=properties or [],
            source=source,
        )

    def select(self, name: str, names: Set[str]) -> bool:
        """
        Tells whether we should select an object or not, given its name.

        If the set of names is not empty, we check against it, otherwise we check against filters.

        Arguments:
            name: The name of the object to select or not.
            names: An explicit list of names to select.

        Returns:
            Yes or no.
        """
        if names:
            return name in names
        return not self.filter_name_out(name)

    @lru_cache(maxsize=None)
    def filter_name_out(self, name: str) -> bool:
        if not self.filters:
            return False
        keep = True
        for f, regex in self.filters:
            is_matching = bool(regex.search(name))
            if is_matching:
                if str(f).startswith("!"):
                    is_matching = not is_matching
                keep = is_matching
        return not keep
