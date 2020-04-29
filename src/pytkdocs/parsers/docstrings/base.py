import inspect
from abc import ABCMeta, abstractmethod
from typing import Any, List, Optional, Tuple

empty = inspect.Signature.empty


class AnnotatedObject:
    """A helper class to store information about an annotated object."""

    def __init__(self, annotation, description):
        self.annotation = annotation
        self.description = description


class Parameter(AnnotatedObject):
    """A helper class to store information about a signature parameter."""

    def __init__(self, name, annotation, description, kind, default=empty):
        super().__init__(annotation, description)
        self.name = name
        self.kind = kind
        self.default = default

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Parameter({self.name}, {self.annotation}, {self.description}, {self.kind}, {self.default})>"

    @property
    def is_optional(self):
        return self.default is not empty

    @property
    def is_required(self):
        return not self.is_optional

    @property
    def is_args(self):
        return self.kind is inspect.Parameter.VAR_POSITIONAL

    @property
    def is_kwargs(self):
        return self.kind is inspect.Parameter.VAR_KEYWORD

    @property
    def default_string(self):
        if self.is_kwargs:
            return "{}"
        elif self.is_args:
            return "()"
        elif self.is_required:
            return ""
        return repr(self.default)


class Section:
    """A helper class to store a docstring section."""

    class Type:
        MARKDOWN = "markdown"
        PARAMETERS = "parameters"
        EXCEPTIONS = "exceptions"
        RETURN = "return"

    def __init__(self, section_type, value):
        self.type = section_type
        self.value = value

    def __str__(self):
        return self.type

    def __repr__(self):
        return f"<Section(type={self.type!r})>"


class Parser(metaclass=ABCMeta):
    """
    A class to parse docstrings.

    It is instantiated with an object's path, docstring, signature and return type.

    The `parse` method then returns structured data,
    in the form of a list of [`Section`][pytkdocs.parsers.docstrings.Section]s.
    It also return the list of errors that occurred during parsing.
    """

    def __init__(self) -> None:
        """Initialization method."""
        self.object_path = ""
        self.object_signature: Optional[inspect.Signature] = None
        self.object_type = None
        self.errors: List[str] = []

    def set_state(
        self, object_path: str, object_signature: Optional[inspect.Signature], object_type: Optional[Any],
    ):
        self.errors = []
        self.object_path = object_path
        self.object_signature = object_signature
        self.object_type = object_type

    def reset_state(self):
        self.object_path = ""
        self.object_signature = None
        self.object_type = None

    def parse(
        self,
        docstring: str,
        object_path: str,
        object_signature: Optional[inspect.Signature] = None,
        object_type: Optional[Any] = None,
    ) -> Tuple[List[Section], List[str]]:
        self.set_state(object_path, object_signature, object_type)
        sections = self.parse_sections(docstring)
        errors = self.errors
        self.reset_state()
        return sections, errors

    def error(self, message):
        self.errors.append(f"{self.object_path}: {message}")

    @abstractmethod
    def parse_sections(self, docstring: str) -> List[Section]:
        raise NotImplementedError
