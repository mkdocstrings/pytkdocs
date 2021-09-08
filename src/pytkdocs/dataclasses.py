import enum
from typing import Dict, Set, Union


class Kind(enum.Enum):
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    DATA = "data"


class Object:
    kind = None

    def __init__(self, name, lineno=None, endlineno=None) -> None:
        self.name = name
        self.lineno = lineno
        self.endlineno = endlineno
        self.parent = None
        self.members: Dict[str, Union[Module, Class, Function, Data]] = {}
        self.labels: Set[str] = set()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.name!r}, {self.lineno!r}, {self.endlineno!r})>"

    def __setitem__(self, key, value):
        if isinstance(key, str):
            if not key:
                raise ValueError("cannot set self (empty key)")
            parts = key.split(".", 1)
        else:
            parts = key
        if not parts:
            raise ValueError("cannot set self (empty parts)")
        if len(parts) == 1:
            self.members[parts[0]] = value
            value.parent = self
        else:
            self.members[parts[0]][parts[1]] = value

    def __getitem__(self, key):
        if isinstance(key, str):
            if not key:
                return self
            parts = key.split(".", 1)
        else:
            parts = key
        if not parts:
            return self
        if len(parts) == 1:
            return self.members[parts[0]]
        return self.members[parts[0]][parts[1]]

    @property
    def module(self):
        if isinstance(self, Module):
            return self
        if self.parent:
            return self.parent.module
        raise ValueError

    @property
    def filepath(self):
        return self.module.filepath

    @property
    def path(self):
        if not self.parent:
            return self.name
        return ".".join((self.parent.path, self.name))

    def as_dict(self, full=False):
        base = {
            "name": self.name,
            "members": [member.as_dict(full) for member in self.members.values()],
            "labels": self.labels,
            "kind": self.kind,
        }
        if self.lineno:
            base["lineno"] = self.lineno
        if self.endlineno:
            base["endlineno"] = self.endlineno

        if full:
            base.update(
                {
                    "filepath": str(self.filepath),
                    "path": self.path,
                }
            )

        return base


class Module(Object):
    kind = Kind.MODULE

    def __init__(self, name, lineno=None, endlineno=None, filepath=None) -> None:
        super().__init__(name, lineno=lineno, endlineno=endlineno)
        self._filepath = filepath

    def __repr__(self) -> str:
        return f"<Module({self._filepath!r})>"

    @property
    def filepath(self):
        return self._filepath

    @property
    def is_folder(self):
        return self.parent and not self.filepath

    @property
    def is_package(self):
        return not self.parent and self.filepath and self.filepath.name == "__init__.py"

    @property
    def is_subpackage(self):
        return self.parent and self.filepath and self.filepath.name == "__init__.py"

    @property
    def is_namespace_package(self):
        return not self.parent and not self.filepath

    @property
    def is_namespace_subpackage(self):
        return (
            self.parent
            and not self.filepath
            and self.parent.is_namespace_subpackage
            or self.parent.is_namespace_package
        )

    def as_dict(self, full):
        base = super().as_dict(full=full)
        base["filepath"] = str(self.filepath) if self.filepath else None
        return base


class Class(Object):
    kind = Kind.CLASS


class Function(Object):
    kind = Kind.FUNCTION


class Data(Object):
    kind = Kind.DATA
