import importlib
import inspect
import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Tuple, Union

from pytkdocs.parsers.docstrings import parse

from .properties import NAME_CLASS_PRIVATE, NAME_PRIVATE, NAME_SPECIAL

ObjectUnion = Union["Attribute", "Method", "Function", "Module", "Class"]


class Object:
    """
    Generic class to store information about a Python object.

    Each instance additionally stores references to its children, grouped by category.
    """

    NAME_PROPERTIES = []
    TOC_SIGNATURE = ""

    def __init__(
        self,
        name: str,
        path: str,
        file_path: str,
        docstring: Optional[str] = None,
        properties: Optional[List[str]] = None,
        source: Optional[Tuple[int, List[str]]] = None,
    ) -> None:
        """

        Parameters:
            name: The object name, like `__init__` or `MyClass`.
            path: The object dotted-path, like `package.submodule.class.inner_class.method`.
            file_path: The full file path of the object's module, like `/full/path/to/package/submodule.py`.
            docstring: A `Docstring` instance
            properties: A list of properties like `special`, `classmethod`, etc.
            source: A tuple with the object source code lines as a list, and the starting line in the object's module.
        """
        self.name = name
        self.path = path
        self.file_path = file_path
        self.docstring = docstring
        self.properties = properties or []
        self.parent = None
        self.source = source

        self._path_map = {self.path: self}

        self.attributes: List[Attribute] = []
        """List of all the object's attributes."""
        self.methods: List[Method] = []
        """List of all the object's methods."""
        self.functions: List[Function] = []
        """List of all the object's functions."""
        self.modules: List[Module] = []
        """List of all the object's submodules."""
        self.classes: List[Class] = []
        """List of all the object's classes."""
        self.children: List[ObjectUnion] = []
        """List of all the object's children."""

    def __str__(self):
        return self.path

    @property
    def is_module(self):
        return isinstance(self, Module)

    @property
    def is_class(self):
        return isinstance(self, Class)

    @property
    def is_function(self):
        return isinstance(self, Function)

    @property
    def is_method(self):
        return isinstance(self, Method)

    @property
    def is_attribute(self):
        return isinstance(self, Attribute)

    @property
    def category(self):
        return self.__class__.__name__.lower()

    @property
    def root(self):
        obj = self
        while obj.parent:
            obj = obj.parent
        return obj

    @property
    def relative_file_path(self):
        top_package_name = self.path.split(".", 1)[0]
        try:
            top_package = sys.modules[top_package_name]
        except KeyError:
            try:
                importlib.import_module(top_package_name)
            except ImportError:
                return ""
            top_package = sys.modules[top_package_name]
        top_package_path = Path(inspect.getabsfile(top_package)).parent
        try:
            return str(Path(self.file_path).relative_to(top_package_path.parent))
        except ValueError:
            return ""

    @property
    def name_to_check(self):
        return self.name

    @property
    def name_properties(self) -> List[str]:
        properties = []
        for prop, predicate in self.NAME_PROPERTIES:
            if predicate(self.name_to_check):
                properties.append(prop)
        return properties

    @property
    def parent_path(self) -> str:
        """The parent's path, computed from the current path."""
        return self.path.rsplit(".", 1)[0]

    def add_child(self, obj: ObjectUnion) -> None:
        """
        Add an object as a child of this object.

        Parameters:
            obj: An instance of documented object.
        """
        if obj.parent_path != self.path:
            return

        self.children.append(obj)
        if obj.is_module:
            self.modules.append(obj)
        elif obj.is_class:
            self.classes.append(obj)
        elif obj.is_function:
            self.functions.append(obj)
        elif obj.is_method:
            self.methods.append(obj)
        elif obj.is_attribute:
            self.attributes.append(obj)
        obj.parent = self

        self._path_map[obj.path] = obj

    def add_children(self, children: List[ObjectUnion]) -> None:
        """Add a list of objects as children of this object."""
        for child in children:
            self.add_child(child)

    def dispatch_attributes(self, attributes: List["Attribute"]) -> None:
        for attribute in attributes:
            try:
                attach_to = self._path_map[attribute.parent_path]
            except KeyError:
                pass
            else:
                attach_to.attributes.append(attribute)
                attach_to.children.append(attribute)
                attribute.parent = attach_to

    def parse_all_docstring(self):
        signature = None
        if hasattr(self, "signature"):
            signature = self.signature
        attr_type = None
        if hasattr(self, "type"):
            attr_type = self.type
        sections, errors = parse(self.path, self.docstring, signature, attr_type)
        self.docstring_sections = sections
        self.docstring_errors = errors
        for child in self.children:
            child.parse_all_docstring()

    @property
    @lru_cache()
    def has_contents(self):
        return bool(self.docstring or not self.parent or any(c.has_contents for c in self.children))


class Module(Object):
    NAME_PROPERTIES = [NAME_SPECIAL, NAME_PRIVATE]

    @property
    def file_name(self):
        return os.path.splitext(os.path.basename(self.file_path))[0]

    @property
    def name_to_check(self):
        return self.file_name


class Class(Object):
    NAME_PROPERTIES = [NAME_PRIVATE]


class Function(Object):
    NAME_PROPERTIES = [NAME_PRIVATE]

    def __init__(self, *args, signature=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.signature = signature


class Method(Object):
    NAME_PROPERTIES = [NAME_SPECIAL, NAME_PRIVATE]

    def __init__(self, *args, signature=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.signature = signature


class Attribute(Object):
    NAME_PROPERTIES = [NAME_SPECIAL, NAME_CLASS_PRIVATE, NAME_PRIVATE]

    def __init__(self, *args, attr_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = attr_type


class Source:
    def __init__(self, lines, line_start):
        self.code = "".join(lines)
        self.line_start = line_start
