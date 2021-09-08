import json
from pathlib import Path

from pytkdocs.dataclasses import Class, Data, Function, Kind, Module


class Encoder(json.JSONEncoder):
    def __init__(self, *args, full=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.full = full

    def default(self, obj):
        if hasattr(obj, "as_dict"):
            return obj.as_dict(self.full)
        if isinstance(obj, Kind):
            return obj.value
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)


def decoder(obj_dict):
    if "kind" in obj_dict:
        kind = Kind(obj_dict["kind"])
        if kind == Kind.MODULE:
            module = Module(obj_dict["name"], obj_dict["lineno"], obj_dict["endlineno"], Path(obj_dict["filepath"]))
            for member in obj_dict.get("members", []):
                module[member.name] = member
            return module
        elif kind == Kind.CLASS:
            class_ = Class(obj_dict["name"], obj_dict["lineno"], obj_dict["endlineno"])
            for member in obj_dict.get("members", []):
                class_[member.name] = member
            return class_
        elif kind == Kind.FUNCTION:
            return Function(obj_dict["name"], obj_dict["lineno"], obj_dict["endlineno"])
        elif kind == Kind.DATA:
            return Data(obj_dict["name"], obj_dict["lineno"], obj_dict["endlineno"])
    return obj_dict
