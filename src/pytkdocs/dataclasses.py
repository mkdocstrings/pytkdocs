from typing import Dict, Set, Union


class Object:
    def __init__(self, filepath, name, starting_line=None, ending_line=None) -> None:
        self.filepath = filepath
        self.name = name
        self.starting_line = starting_line
        self.ending_line = ending_line
        self.members: Dict[str, Union[Package, Module, Class, Function, Data]] = {}
        self.labels: Set[str] = set()

    def __setitem__(self, key, value):
        parts = key.split(".")
        if len(parts) == 1:
            self.members[key] = value
        else:
            obj = self.members
            for part in parts[:-1]:
                obj = obj[part].members
            obj[parts[-1]] = value

    def __getitem__(self, key):
        parts = key.split(".", 1)
        if len(parts) == 1:
            return self.members[key]
        return self.members[parts[0]][parts[1]]


class Package(Object):
    pass


class Module(Object):
    pass


class Class(Object):
    pass


class Function(Object):
    pass


class Data(Object):
    pass
