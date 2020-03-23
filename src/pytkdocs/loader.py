"""
This module is responsible for loading the documentation from Python objects.
"""

import importlib
import inspect
import pkgutil
import re
import textwrap
from functools import lru_cache
from types import ModuleType
from typing import Any, Callable, Optional, Tuple, Type, Union

from .objects import Attribute, Class, Function, Method, Module
from .parsers.attributes import get_attributes
from .parsers.docstrings import Docstring
from .properties import RE_SPECIAL


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
        module, obj = import_object(import_string)
        attributes = get_attributes(module)
        if inspect.ismodule(obj):
            root_object = self.get_module_documentation(obj)
        elif inspect.isclass(obj):
            root_object = self.get_class_documentation(obj, module)
        elif inspect.isfunction(obj):
            root_object = self.get_function_documentation(obj, module)
        else:
            raise ValueError(f"{obj}:{type(obj)} not yet supported")
        root_object.dispatch_attributes([a for a in attributes if not self.filter_name_out(a.name)])
        return root_object

    def get_module_documentation(self, module: ModuleType) -> Module:
        path = module.__name__
        name = path.split(".")[-1]
        root_object = Module(
            name=name, path=path, file_path=module.__file__, docstring=Docstring(inspect.getdoc(module))
        )
        for member_name, member in (m for m in inspect.getmembers(module) if not self.filter_name_out(m[0])):
            if inspect.isclass(member) and inspect.getmodule(member) == module:
                root_object.add_child(self.get_class_documentation(member, module))
            elif inspect.isfunction(member) and inspect.getmodule(member) == module:
                root_object.add_child(self.get_function_documentation(member, module))

        try:
            package_path = module.__path__
        except AttributeError:
            pass
        else:
            for _, modname, _ in pkgutil.iter_modules(package_path):
                if not self.filter_name_out(modname):
                    parent, submodule = import_object(f"{path}.{modname}")
                    root_object.add_child(self.get_module_documentation(submodule))

        return root_object

    def get_class_documentation(self, class_: Type[Any], module: Optional[ModuleType] = None) -> Class:
        if module is None:
            module = inspect.getmodule(class_)
        class_name = class_.__name__
        path = f"{module.__name__}.{class_name}"
        try:
            file_path = module.__file__
        except AttributeError:
            self.errors.append(f"Couldn't get file path of module '{str(module)}'")
            file_path = ""
        try:
            signature = inspect.signature(class_)
        except ValueError as error:
            self.errors.append(f"Couldn't get signature for '{class_name}': {error}")
            signature = inspect.Signature()
        docstring = Docstring(textwrap.dedent(class_.__doc__ or ""), signature)
        root_object = Class(name=class_name, path=path, file_path=file_path, docstring=docstring,)

        for member_name, member in sorted(filter(lambda m: not self.filter_name_out(m[0]), class_.__dict__.items())):
            if inspect.isclass(member):
                root_object.add_child(self.get_class_documentation(member))
                continue

            member_class = properties = signature = None
            member_path = f"{path}.{member_name}"
            actual_member = getattr(class_, member_name)
            docstring = inspect.getdoc(actual_member) or ""
            try:
                source = inspect.getsourcelines(actual_member)
            except OSError as error:
                self.errors.append(f"Couldn't read source for '{member_path}': {error}")
                source = ""
            except TypeError:
                source = ""

            if isinstance(member, classmethod):
                properties = ["classmethod"]
                member_class = Method
                signature = inspect.signature(actual_member)
            elif isinstance(member, staticmethod):
                properties = ["staticmethod"]
                member_class = Method
                signature = inspect.signature(actual_member)
            elif isinstance(member, type(lambda: 0)):  # regular method
                if RE_SPECIAL.match(member_name):
                    parent_classes = class_.__mro__[1:]
                    for parent_class in parent_classes:
                        try:
                            parent_member = getattr(parent_class, member_name)
                        except AttributeError:
                            continue
                        else:
                            if docstring == inspect.getdoc(parent_member):
                                docstring = ""
                            break
                member_class = Method
                signature = inspect.signature(actual_member)
            elif isinstance(member, property):
                properties = ["property", "readonly" if member.fset is None else "writable"]
                try:
                    signature = inspect.signature(actual_member.fget)
                except ValueError as error:
                    # TODO: this happens with members of classes inheriting from typing.NamedTuple.
                    # It's special treatment that must be implemented for such cases (like Pydantic models).
                    self.errors.append(f"Couldn't get signature for '{member_path}': {error}")
                    signature = None
                member_class = Attribute

            if member_class:
                root_object.add_child(
                    member_class(
                        name=member_name,
                        path=member_path,
                        file_path=file_path,
                        docstring=Docstring(docstring, signature),
                        properties=properties,
                        source=source,
                    )
                )
        return root_object

    def get_function_documentation(self, function: Callable, module: Optional[ModuleType] = None) -> Function:
        if module is None:
            module = inspect.getmodule(function)
        function_name = function.__name__
        path = f"{module.__name__}.{function_name}"
        return Function(
            name=function_name,
            path=path,
            file_path=module.__file__,
            docstring=Docstring(inspect.getdoc(function) or "", inspect.signature(function)),
            source=inspect.getsourcelines(function),
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


def import_object(path: str) -> Tuple[ModuleType, Any]:
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

    obj_parent_modules = path.split(".")
    objects = []

    while True:
        try:
            parent_module_path = ".".join(obj_parent_modules)
            parent_module = importlib.import_module(parent_module_path)
            break
        except ImportError:
            if len(obj_parent_modules) == 1:
                raise ImportError("No module named '%s'" % obj_parent_modules[0])
            objects.insert(0, obj_parent_modules.pop(-1))

    current_object = parent_module
    for obj in objects:
        current_object = getattr(current_object, obj)
    module = inspect.getmodule(current_object)
    return module, current_object
