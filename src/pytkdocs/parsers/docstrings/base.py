"""The base module for docstring parsing."""

import inspect
from abc import ABCMeta, abstractmethod
from typing import Any, List, Optional, Tuple, Union

empty = inspect.Signature.empty


class AnnotatedObject:
    """A helper class to store information about an annotated object."""

    def __init__(self, annotation: Any, description: str) -> None:
        """
        Initialization method.

        Arguments:
            annotation: The object's annotation.
            description: The object's description.
        """
        self.annotation = annotation
        self.description = description


class Parameter(AnnotatedObject):
    """A helper class to store information about a signature parameter."""

    def __init__(self, name: str, annotation: Any, description: str, kind: Any, default: Any = empty) -> None:
        """
        Initialization method.

        Arguments:
            name: The parameter's name.
            annotation: The parameter's annotation.
            description: The parameter's description.
            kind: The parameter's kind (positional only, keyword only, etc.).
            default: The parameter's default value.
        """
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
        """Is this parameter optional?"""
        return self.default is not empty

    @property
    def is_required(self):
        """Is this parameter required?"""
        return not self.is_optional

    @property
    def is_args(self):
        """Is this a positional parameter?"""
        return self.kind is inspect.Parameter.VAR_POSITIONAL

    @property
    def is_kwargs(self):
        """Is this a keyword parameter?"""
        return self.kind is inspect.Parameter.VAR_KEYWORD

    @property
    def default_string(self):
        """The default value as a string."""
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
        """The possible section types."""

        MARKDOWN = "markdown"
        PARAMETERS = "parameters"
        EXCEPTIONS = "exceptions"
        RETURN = "return"

    def __init__(
        self, section_type: str, value: Union[str, List[Parameter], List[AnnotatedObject], AnnotatedObject]
    ) -> None:
        """
        Initialization method.

        Arguments:
            section_type: The type of the section, from the [`Type`][pytkdocs.parsers.docstrings.base.Section.Type] enum.
            value: The section value.
        """
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
    in the form of a list of [`Section`][pytkdocs.parsers.docstrings.base.Section]s.
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
    ) -> None:
        """
        Set the state of the parser.

        It is used to make these data available in the `parse_sections` method when implementing a parser.

        Arguments:
            object_path: The object's dotted path.
            object_signature: The object's signature.
            object_type: The object's type.
        """
        self.errors = []
        self.object_path = object_path
        self.object_signature = object_signature
        self.object_type = object_type

    def reset_state(self) -> None:
        """Reset the parser state."""
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
        """
        Parse a docstring and return a list of sections and parsing errors.

        Arguments:
            docstring: The docstring to parse.
            object_path: The object's dotted path.
            object_signature: The object's signature.
            object_type: The object's type.

        Returns:
            A tuple containing the list of sections and the parsing errors.
        """
        self.set_state(object_path, object_signature, object_type)
        sections = self.parse_sections(docstring)
        errors = self.errors
        self.reset_state()
        return sections, errors

    def error(self, message) -> None:
        """
        Record a parsing error.

        Arguments:
            message: A message described the error.
        """
        self.errors.append(f"{self.object_path}: {message}")

    @abstractmethod
    def parse_sections(self, docstring: str) -> List[Section]:
        """
        Parse a docstring as a list of sections.

        Arguments:
            docstring: The docstring to parse.

        Returns:
            A list of [`Section`][pytkdocs.parsers.docstrings.base.Section]s.
        """
        raise NotImplementedError
