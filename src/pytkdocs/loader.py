"""
This module is responsible for loading the documentation from Python objects.
"""

import importlib
import inspect
import pkgutil
import re
import textwrap
from functools import lru_cache
from typing import List, Optional, Union

from .objects import Attribute, Class, Function, Method, Module, Source
from .parsers.attributes import get_attributes
from .properties import RE_SPECIAL


class ObjectNode:
    def __init__(self, obj, name, parent=None):
        self.obj = obj
        self.name = name
        self.parent = parent

    @property
    def dotted_path(self):
        parts = [self.name]
        current = self.parent
        while current:
            parts.append(current.name)
            current = current.parent
        return ".".join(reversed(parts))

    @property
    def file_path(self):
        return inspect.getabsfile(self.root.obj)

    @property
    def root(self):
        if self.parent is not None:
            return self.parent.root
        return self

    def is_module(self):
        return inspect.ismodule(self.obj)

    def is_class(self):
        return inspect.isclass(self.obj)

    def is_function(self):
        return inspect.isfunction(self.obj)

    def is_property(self):
        return isinstance(self.obj, property)

    def parent_is_class(self):
        return self.parent and self.parent.is_class()

    def is_method(self):
        return self.parent_is_class() and isinstance(self.obj, type(lambda: 0))

    def is_staticmethod(self):
        return self.parent_is_class() and isinstance(self.parent.obj.__dict__.get(self.name, None), staticmethod)

    def is_classmethod(self):
        return self.parent_is_class() and isinstance(self.parent.obj.__dict__.get(self.name, None), classmethod)


def get_object_tree(path: str) -> ObjectNode:
    """
    Transform a path into an actual Python object.

    The path can be arbitrary long. You can pass the path to a package,
    a module, a class, a function or a global variable, as deep as you
    want, as long as the deepest module is importable through
    ``importlib.import_module`` and each object is obtainable through
    the ``getattr`` method. Local objects will not work.

    Args:
        path: the dot-separated path of the object.

    Returns:
        The imported module and obtained object.
    """
    if not path:
        raise ValueError(f"path must be a valid Python path, not {path}")

    # We will try to import the longest dotted-path first.
    # If it fails, we remove the right-most part and put it in a list of "objects", used later.
    # We loop until we find the deepest importable submodule.
    obj_parent_modules = path.split(".")
    objects = []

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
        current_node.child = ObjectNode(obj, obj_name, parent=current_node)
        current_node = current_node.child

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
    """Class that contains the object documentation loading mechanisms."""

    def __init__(self, filters=None):
        if not filters:
            filters = []
        self.filters = [(f, re.compile(f.lstrip("!"))) for f in filters]

        self.errors = []

    def get_object_documentation(self, import_string: str) -> Union[Attribute, Method, Function, Module, Class]:
        """
        Documenting to see return type.

        Return:
            The object with all its children populated.
        """
        leaf = get_object_tree(import_string)
        attributes = get_attributes(leaf.root.obj)
        if leaf.is_module():
            root_object = self.get_module_documentation(leaf)
        elif leaf.is_class():
            root_object = self.get_class_documentation(leaf)
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
                if attribute.path == import_string:
                    return attribute
            raise ValueError(f"{import_string}: {type(leaf.obj)} not yet supported")
        root_object.dispatch_attributes([a for a in attributes if not self.filter_name_out(a.name)])
        root_object.parse_all_docstring()
        return root_object

    def get_module_documentation(self, node: ObjectNode) -> Module:
        module = node.obj
        path = node.dotted_path
        name = path.split(".")[-1]
        root_object = Module(name=name, path=path, file_path=node.file_path, docstring=inspect.getdoc(module))
        for member_name, member in inspect.getmembers(module):
            if self.filter_name_out(member_name):
                continue

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
                if not self.filter_name_out(modname):
                    leaf = get_object_tree(f"{path}.{modname}")
                    root_object.add_child(self.get_module_documentation(leaf))

        return root_object

    def get_class_documentation(self, node: ObjectNode) -> Class:
        class_ = node.obj
        docstring = textwrap.dedent(class_.__doc__ or "")
        root_object = Class(name=node.name, path=node.dotted_path, file_path=node.file_path, docstring=docstring)

        for member_name, member in class_.__dict__.items():
            if member is type or member is object:
                continue

            if self.filter_name_out(member_name):
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
        function = node.obj
        path = node.dotted_path

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
        prop = node.obj
        path = node.dotted_path
        properties = ["property", "readonly" if prop.fset is None else "writable"]

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
        return self.get_method_documentation(node, ["classmethod"])

    def get_staticmethod_documentation(self, node: ObjectNode) -> Method:
        return self.get_method_documentation(node, ["staticmethod"])

    def get_regular_method_documentation(self, node: ObjectNode) -> Method:
        method = self.get_method_documentation(node)
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

    def get_method_documentation(self, node: ObjectNode, properties: Optional[List[str]] = None):
        method = node.obj
        path = node.dotted_path

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

    @lru_cache(maxsize=None)
    def filter_name_out(self, name: str) -> bool:
        if not self.filters:
            return False
        keep = True
        for f, regex in self.filters:
            is_matching = bool(regex.match(name))
            if is_matching:
                if str(f).startswith("!"):
                    is_matching = not is_matching
                keep = is_matching
        return not keep
