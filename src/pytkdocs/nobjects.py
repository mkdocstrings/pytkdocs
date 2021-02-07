import enum
import importlib
import inspect
from functools import cached_property
from typing import Any, List, Optional


"""
real module path is needed to get the source code of attributes and their docstrings
ironically, inspect cannot get the module for certain variables, mainly builtin ones

## Constants with builtin types

```python
# module a.py
from b import v1, v2
```

```python
# module b.py
v1 = 0
\"\"\"Description of v1.\"\"\"

v2 = "hello"
\"\"\"Description of v2.\"\"\"
```

```markdown
::: a.v1

::: a.v2
```

## More nested attributes

```python
# b.py
import enum


class E(enum.Enum):
    A = 0
    \"\"\"Description of A.\"\"\"


class Z:
    A = 0
    \"\"\"Description of A.\"\"\"
```

```python
# module a.py
from b import E, Z

class N:
    v1 = E.A
    v2 = Z.A
```

```markdown
::: a.N.v1

::: a.N.v2
```
"""


class Order(enum.Enum):
    source = "source"
    name = "name"
    category = "category"
    category_name = "category+name"
    category_source = "category+source"


class CategoryOrder(list):
    pass


def get_module_and_objects(path, new_path_syntax: bool = False):
    if ":" in path or new_path_syntax:
        try:
            module_path, object_path = path.split(":")
        except ValueError:  # no colon
            module_path, objects = path, []
        else:
            objects = object_path.split(".")

        # let the ImportError bubble up
        parent_module = importlib.import_module(module_path)

    else:
        # We will try to import the longest dotted-path first.
        # If it fails, we remove the right-most part and put it in a list of "objects", used later.
        # We loop until we find the deepest importable submodule.
        obj_parent_modules = path.split(".")

        while True:
            module_path = ".".join(obj_parent_modules)
            try:
                parent_module = importlib.import_module(module_path)
            except ImportError as error:
                if len(obj_parent_modules) == 1:
                    raise ImportError(
                        f"Importing '{path}' failed, possible causes are:\n"
                        f"- an exception happened while importing\n"
                        f"- an element in the path does not exist",
                    ) from error
                objects.insert(0, obj_parent_modules.pop(-1))
            else:
                break

    return parent_module, objects

# New path syntax: the new path syntax uses a colon to separate the
# modules (to import) from the objects (to get with getattr).
# It's easier to deal with, and it naturally improves error handling.
# At first, we default to the old syntax, then at some point we will
# default to the new syntax, and later again we will drop the old syntax.
def get_object_tree(path: str, new_path_syntax: bool = False) -> None:
    """
    Import the object and populate some instance variables.

    The path can be arbitrary long. You can pass the path to a package,
    a module, a class, a function or a global variable, as deep as you
    want, as long as the deepest module is importable through
    `importlib.import_module` and each object is obtainable through
    the `getattr` method. It is not possible to load local objects.

    Args:
        path: The dot/colon-separated path of the object.
        new_path_syntax: Whether to use the "colon" syntax for the path.

    Raises:
        ValueError: When the path is not valid (evaluates to `False`).
        ImportError: When the object or its parent module could not be imported.

    Returns:
        The leaf node representing the object and its parents.
    """
    if not path:
        raise ValueError(f"path must be a valid Python path, not {path}")

    objects: List[str] = []
    parent_module, objects = get_module_and_objects(path, new_path_syntax)

    # We now have the module containing the desired object.
    # We will build the object tree by iterating over the previously stored objects names
    # and trying to get them as attributes.
    parents = module_path.split(".")
    parent = None    
    for parent_name in parents:
        parent_path = f"{parent.path}.{parent_name}" if parent else parent_name
        child = Object(
            name=parent_name,
            value=importlib.import_module(parent_path),
            parent=parent,
        )
        parent = child

    for child_name in objects:
        actual_obj = getattr(parent.value, child_name)
        child = MetaObject(name=child_name, value=actual_obj, parent=parent)
        parent = child

    return child


def get_object_value(path)


empty = object()


class Object:
    def __init__(
        self,
        
        path=None,
        name=None,
        value=empty,  # can be used as "default"
        
        source=None, # file.absolute, file.relative, code, line
        docstring=None,  # raw, parsed.sections, parsed.errors
        
        modules=None,
        functions=None,
        classes=None,
        methods=None,
        attributes=None,

        parent=None,
        children=None,

        # using tags to filter:
        static_methods=None,
        class_methods=None,
        properties=None,
        # tags:
        #   classes, functions, methods:
        #     decorated
        #   anything (names):
        #   __special__, __private (name mangling), _protected
        #   properties:
        #     read-only, writable
        #   attributes:
        #     django model field, pydantic field, marshmallow field, etc.
        #   classes:
        #     django model, pydantic model, marshmallow model, etc.
        #   modules:
        #     namespaced?

    ) -> None:
        self._path = path
        self._name = name
        self._value = value
        self._source = source
        self._docstring = docstring
        self._modules = modules
        self._functions = functions
        self._classes = classes
        self._methods = methods
        self._attributes = attributes
        self._parent = parent
        self._children = children

    @property
    def name(self):
        if self._name is None:
            self._name = self.dpath.rsplit(".", 1)[1]
        return self._name

    @property
    def path(self):
        if self._path is None:
            if self._name is None:
                raise ValueError("Cannot infer path of object without name")
            if self._parent is None:
                self._path = self._name
            else:
                self._path = f"{self._parent.path}.{self._name}"
        return self._path

    @cached_property
    def dpath(self):
        return self.path.replace(":", ".")

    @property
    def value(self):
        if self._value is empty:
            self._value = get_object_value(self.path)
        return self._value

    @cached_property
    def module(self):
        module = inspect.getmodule(self.value)
        if module is None and self._parent:
            return self._parent.module
        return module

    def modules(self):
        pass

    def classes(self):
        pass

    def functions(self):
        pass

    def methods(self):
        pass

    def properties(self):
        pass

    def attributes(self):
        pass

    def children(self, order_by):
        pass


class Module(Object):
    def __init__(self, path, obj=None, parent: "Module" = None):
        super().__init__(path)
        self.obj = obj
        self.parent: Module = parent

    @property
    def file_path(self) -> str:
        """
        Return the object's module file path.

        Returns:
            The object's module file path.
        """
        return inspect.getabsfile(self.root.obj)

    @property
    def path(self) -> str:
        """
        Return the Python dotted path to the object.

        Returns:
            The Python dotted path to the object.
        """
        parts = [self.name]
        current = self.parent
        while current:
            parts.append(current.name)
            current = current.parent
        return ".".join(reversed(parts))

    @property
    def root(self) -> "ObjectNode":
        """
        Return the root of the tree.

        Returns:
            The root of the tree.
        """
        if self.parent is not None:
            return self.parent.root
        return self

class Function(Object):
    pass


class Class(Object):
    pass


class Method(Object):
    pass


class Property(Object):
    pass


class Attribute(Object):
    pass