"""
This module defines the documented objects classes:

- the generic [`Object`][pytkdocs.objects.Object] class
- the [`Module`][pytkdocs.objects.Module] class
- the [`Class`][pytkdocs.objects.Class] class
- the [`Method`][pytkdocs.objects.Method] class
- the [`Function`][pytkdocs.objects.Function] class
- the [`Attribute`][pytkdocs.objects.Attribute] class

Note that properties are considered attributes, because they are used like such.

It also defines a convenient [`Source`][pytkdocs.objects.Source] class to represent source code.
"""

import importlib
import inspect
import os
import sys
from abc import ABCMeta
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Union

from pytkdocs.parsers.docstrings import parse

from .properties import NAME_CLASS_PRIVATE, NAME_PRIVATE, NAME_SPECIAL, ApplicableNameProperty


class Source:
    """
    Helper class to represent source code.

    It is simply used to wrap the result of
    [`inspect.getsourceslines`](https://docs.python.org/3/library/inspect.html#inspect.getsourcelines).
    """

    def __init__(self, lines: Union[str, List[str]], line_start: int) -> None:
        """
        Arguments:
            lines: A list of strings. The strings should have trailing newlines.
            line_start: The line number of where the code starts in the file.
        """
        if isinstance(lines, list):
            code = "".join(lines)
        else:
            code = lines
        self.code = code
        """The code, as a single string."""
        self.line_start = line_start
        """The first line number."""


class Object(metaclass=ABCMeta):
    """
    A base class to store information about a Python object.

    Each instance additionally stores references to its children, grouped by category.
    """

    NAME_PROPERTIES: List[ApplicableNameProperty] = []
    """
    The properties that we can apply to the object based on its name.

    The applicable properties vary from one subclass of `Object` to another.
    """

    def __init__(
        self,
        name: str,
        path: str,
        file_path: str,
        docstring: str = "",
        properties: Optional[List[str]] = None,
        source: Optional[Source] = None,
    ) -> None:
        """
        Arguments:
            name: The object's name.
            path: The object's dotted-path.
            file_path: The file path of the object's direct parent module.
            docstring: The object's docstring.
            properties: The object's properties.
            source: The object's source code.
        """

        self.name = name
        """The object's name."""
        self.path = path
        """The object's dotted-path."""
        self.file_path = file_path
        """The file path of the object's direct parent module."""
        self.docstring = docstring
        """The object's docstring."""
        self.properties = properties or []
        """The object's properties."""
        self.parent: Optional[Object] = None
        """The object's parent (another instance of a subclass of `Object`)."""
        self.source = source
        """The object's source code."""

        self._path_map = {self.path: self}

        self.attributes: List[Attribute] = []
        """The list of all the object's attributes."""
        self.methods: List[Method] = []
        """The list of all the object's methods."""
        self.functions: List[Function] = []
        """The list of all the object's functions."""
        self.modules: List[Module] = []
        """The list of all the object's submodules."""
        self.classes: List[Class] = []
        """The list of all the object's classes."""
        self.children: List[Object] = []
        """The list of all the object's children."""

    def __str__(self) -> str:
        return self.path

    @property
    def is_module(self) -> bool:
        """Is this object a module?"""
        return isinstance(self, Module)

    @property
    def is_class(self) -> bool:
        """Is this object a class?"""
        return isinstance(self, Class)

    @property
    def is_function(self) -> bool:
        """Is this object a function?"""
        return isinstance(self, Function)

    @property
    def is_method(self) -> bool:
        """Is this object a method?"""
        return isinstance(self, Method)

    @property
    def is_attribute(self) -> bool:
        """Is this object an attribute?"""
        return isinstance(self, Attribute)

    @property
    def category(self) -> str:
        """The object's category: module, class, function, method or attribute."""
        return self.__class__.__name__.lower()

    @property
    def root(self) -> "Object":
        """The object's root (top-most parent)."""
        obj = self
        while obj.parent:
            obj = obj.parent
        return obj  # type: ignore

    @property
    def relative_file_path(self) -> str:
        """
        The relative file path of the object.

        It is the relative path to the object's module,
        starting at the path of the top-most package it is contained in.

        For example:

        - package is `a`
        - package absolute path is `/abs/path/to/a`
        - module is `a.b.c`
        - object is `c` or anything defined in `c`
        - relative file path is `a/b/c.py`

        If the relative file path cannot be determined, the value returned is `""` (empty string).
        """
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
    def name_to_check(self) -> str:
        """The attribute to check against name properties regular expressions (private, class-private, special)."""
        return self.name

    @property
    def name_properties(self) -> List[str]:
        """The object's name properties (private, class-private, special)."""
        properties = []
        for prop, predicate in self.NAME_PROPERTIES:
            if predicate(self.name_to_check):
                properties.append(prop)
        return properties

    @property
    def parent_path(self) -> str:
        """
        The parent's path, computed from the current path.

        The parent object path is not used: this property is used to see if an object is really related to another one,
        to add it as a child to the other. When we do that, the child doesn't even have a parent.
        """
        return self.path.rsplit(".", 1)[0]

    def add_child(self, obj: "Object") -> None:
        """
        Add an object as a child of this object.

        If the child computed `parent_path` is not equal to this object's path, abort.

        Append the child to the `children` list, and to the right category list.

        Arguments:
            obj: An instance of documented object.
        """
        if obj.parent_path != self.path:
            return

        self.children.append(obj)
        if obj.is_module:
            self.modules.append(obj)  # type: ignore
        elif obj.is_class:
            self.classes.append(obj)  # type: ignore
        elif obj.is_function:
            self.functions.append(obj)  # type: ignore
        elif obj.is_method:
            self.methods.append(obj)  # type: ignore
        elif obj.is_attribute:
            self.attributes.append(obj)  # type: ignore
        obj.parent = self

        self._path_map[obj.path] = obj

    def add_children(self, children: List["Object"]) -> None:
        """
        Add a list of objects as children of this object.

        Arguments:
            children: The list of children to add.
        """
        for child in children:
            self.add_child(child)

    def dispatch_attributes(self, attributes: List["Attribute"]) -> None:
        """
        Dispatch attributes as children of an object and its children given their path.

        If an attribute's path does not correspond to the object or any of its children,
        the attribute is not attached.

        Arguments:
            attributes: The list of attributes to dispatch.
        """
        for attribute in attributes:
            try:
                attach_to = self._path_map[attribute.parent_path]
            except KeyError:
                pass
            else:
                attach_to.attributes.append(attribute)
                attach_to.children.append(attribute)
                attribute.parent = attach_to

    def parse_all_docstring(self) -> None:
        """
        Recursively parse the docstring of this object and its children.

        I hope we can get rid of this code at some point as parsing docstring is not really our purpose.
        """
        signature = None
        if hasattr(self, "signature"):
            signature = self.signature  # type: ignore
        attr_type = None
        if hasattr(self, "type"):
            attr_type = self.type  # type: ignore
        sections, errors = parse(self.path, self.docstring, signature, attr_type)
        self.docstring_sections = sections
        self.docstring_errors = errors
        for child in self.children:
            child.parse_all_docstring()

    @lru_cache()
    def has_contents(self) -> bool:
        """
        Tells if the object has "contents".

        An object has contents when:

        - it is the root of the object tree
        - it has a docstring
        - at least one of its children (whatever the depth) has contents

        The value is cached, so this method should be called last, when the tree doesn't change anymore.
        """
        return bool(self.docstring or not self.parent or any(c.has_contents() for c in self.children))


class Module(Object):
    """A class to store information about a module."""

    NAME_PROPERTIES: List[ApplicableNameProperty] = [NAME_SPECIAL, NAME_PRIVATE]

    @property
    def file_name(self):
        """The base name of the module file, without the extension."""
        return os.path.splitext(os.path.basename(self.file_path))[0]

    @property
    def name_to_check(self):
        return self.file_name


class Class(Object):
    """A class to store information about a class."""

    NAME_PROPERTIES: List[ApplicableNameProperty] = [NAME_PRIVATE]


class Function(Object):
    """
    A class to store information about a function.

    It accepts an additional `signature` argument at instantiation.
    """

    NAME_PROPERTIES: List[ApplicableNameProperty] = [NAME_PRIVATE]

    def __init__(self, *args, signature=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.signature = signature


class Method(Object):
    """
    A class to store information about a method.

    It accepts an additional `signature` argument at instantiation.
    """

    NAME_PROPERTIES: List[ApplicableNameProperty] = [NAME_SPECIAL, NAME_PRIVATE]

    def __init__(self, *args, signature=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.signature = signature


class Attribute(Object):
    """
    A class to store information about an attribute.

    It accepts an additional `attr_type` argument at instantiation.
    """

    NAME_PROPERTIES: List[ApplicableNameProperty] = [NAME_SPECIAL, NAME_CLASS_PRIVATE, NAME_PRIVATE]

    def __init__(self, *args, attr_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = attr_type
