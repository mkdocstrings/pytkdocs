"""The base module for docstring parsing."""

import inspect
from abc import ABCMeta, abstractmethod
from typing import Any, Optional

empty = inspect.Signature.empty


class AnnotatedObject:
    """A helper class to store information about an annotated object."""

    def __init__(self, annotation: Any, description: str) -> None:
        """Initialize the object.

        Arguments:
            annotation: The object's annotation.
            description: The object's description.
        """
        self.annotation = annotation
        self.description = description


class Attribute(AnnotatedObject):
    """A helper class to store information about a documented attribute."""

    def __init__(self, name: str, annotation: Any, description: str) -> None:
        """Initialize the object.

        Arguments:
            name: The attribute's name.
            annotation: The object's annotation.
            description: The object's description.
        """
        super().__init__(annotation, description)
        self.name = name


class Parameter(AnnotatedObject):
    """A helper class to store information about a signature parameter."""

    def __init__(self, name: str, annotation: Any, description: str, kind: Any, default: Any = empty) -> None:
        """Initialize the object.

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
    def is_optional(self) -> bool:
        """Tell if this parameter is optional."""
        return self.default is not empty

    @property
    def is_required(self) -> bool:
        """Tell if this parameter is required."""
        return not self.is_optional

    @property
    def is_args(self) -> bool:
        """Tell if this parameter is positional."""
        return self.kind is inspect.Parameter.VAR_POSITIONAL

    @property
    def is_kwargs(self) -> bool:
        """Tell if this parameter is a keyword."""
        return self.kind is inspect.Parameter.VAR_KEYWORD

    @property
    def default_string(self) -> str:
        """Return the default value as a string."""
        if self.is_kwargs:
            return "{}"
        if self.is_args:
            return "()"
        if self.is_required:
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
        YIELD = "yield"
        EXAMPLES = "examples"
        ATTRIBUTES = "attributes"
        KEYWORD_ARGS = "keyword_args"

    def __init__(self, section_type: str, value: Any) -> None:
        """Initialize the object.

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
    """A class to parse docstrings.

    It is instantiated with an object's path, docstring, signature and return type.

    The `parse` method then returns structured data,
    in the form of a list of [`Section`][pytkdocs.parsers.docstrings.base.Section]s.
    It also return the list of errors that occurred during parsing.
    """

    def __init__(self, **kwargs: Any) -> None:  # noqa: ARG002
        """Initialize the object."""
        self.context: dict = {}
        self.errors: list[str] = []

    def parse(self, docstring: str, context: Optional[dict] = None) -> tuple[list[Section], list[str]]:
        """Parse a docstring and return a list of sections and parsing errors.

        Arguments:
            docstring: The docstring to parse.
            context: Some context helping to parse the docstring.

        Returns:
            A tuple containing the list of sections and the parsing errors.
        """
        self.context = context or {}
        self.errors = []
        sections = self.parse_sections(docstring)
        errors = self.errors
        return sections, errors

    def error(self, message: str) -> None:
        """Record a parsing error.

        Arguments:
            message: A message described the error.
        """
        if self.context["obj"]:
            message = f"{self.context['obj'].path}: {message}"
        self.errors.append(message)

    @abstractmethod
    def parse_sections(self, docstring: str) -> list[Section]:
        """Parse a docstring as a list of sections.

        Arguments:
            docstring: The docstring to parse.

        Returns:
            A list of [`Section`][pytkdocs.parsers.docstrings.base.Section]s.
        """
        raise NotImplementedError


class UnavailableParser:  # noqa: D101
    def __init__(self, message: str) -> None:  # noqa: D107
        self.message = message

    def parse(self, docstring: str, context: Optional[dict] = None) -> tuple[list[Section], list[str]]:  # noqa: ARG002, D102
        context = context or {}
        message = self.message
        if "obj" in context:
            message = f"{context['obj'].path}: {message}"
        return [], [message]

    def __call__(self, *args, **kwargs):  # noqa: ANN003, ANN002, ARG002, D102
        return self
