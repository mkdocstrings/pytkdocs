"""This module defines functions and classes to parse docstrings into structured data."""

import inspect
import re
from textwrap import dedent
from typing import Any, List, Optional, Pattern, Sequence, Tuple

try:
    from typing import GenericMeta  # python 3.6
except ImportError:
    # in 3.7, GenericMeta doesn't exist but we don't need it
    class GenericMeta(type):  # type: ignore
        pass


empty = inspect.Signature.empty


TITLES_PARAMETERS: Sequence[str] = ("args:", "arguments:", "params:", "parameters:")
"""Titles to match for "parameters" sections."""

TITLES_EXCEPTIONS: Sequence[str] = ("raise:", "raises:", "except:", "exceptions:")
"""Titles to match for "exceptions" sections."""

TITLES_RETURN: Sequence[str] = ("return:", "returns:")
"""Titles to match for "returns" sections."""


RE_OPTIONAL: Pattern = re.compile(r"Union\[(.+), NoneType\]")
"""Regular expression to match optional annotations of the form `Union[T, NoneType]`."""

RE_FORWARD_REF: Pattern = re.compile(r"_ForwardRef\('([^']+)'\)")
"""Regular expression to match forward-reference annotations of the form `_ForwardRef('T')`."""

RE_GOOGLE_STYLE_ADMONITION: Pattern = re.compile(r"^(?P<indent>\s*)(?P<type>[\w-]+):((?:\s+)(?P<title>.+))?$")
"""Regular expressions to match lines starting admonitions, of the form `TYPE: [TITLE]`."""


class AnnotatedObject:
    """A helper class to store information about an annotated object."""

    def __init__(self, annotation, description):
        self.annotation = annotation
        self.description = description

    def __str__(self):
        return self.annotation_string

    @property
    def annotation_string(self):
        return annotation_to_string(self.annotation)


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


class DocstringParser:
    """
    A class to parse docstrings.

    It is instantiated with an object's path, docstring, signature and return type.

    The `parse` method then returns structured data,
    in the form of a list of [`Section`][pytkdocs.parsers.docstrings.Section]s.
    It also return the list of errors that occurred during parsing.
    """

    def __init__(
        self,
        path: str,
        docstring: str,
        signature: Optional[inspect.Signature] = None,
        return_type: Optional[Any] = empty,
    ) -> None:
        """
        Arguments:
            path: An object's dotted-path, used to improve error messages.
            docstring: An object's docstring: the docstring to parse.
            signature: An object's signature if any.
            return_type: An object's return type if any. Can be a string or a type.
        """
        self.path = path
        self.docstring = docstring or ""
        self.signature = signature
        self.return_type = return_type
        self.parsing_errors: List[str] = []

    def parse(self, admonitions: bool = True) -> List[Section]:
        """
        Parse a docstring.

        Arguments:
            admonitions: Whether to transform "Google-Style admonitions" to "Markdown admonitions"
                by transforming `Type: [Title]` to `!!! type: ["Title"]`.

        Returns:
             A tuple containing the list of parsed sections and the errors that occurred during parsing.
        """
        sections = []
        current_section = []

        in_code_block = False

        lines = self.docstring.split("\n")
        i = 0

        while i < len(lines):
            line_lower = lines[i].lower()
            if in_code_block:
                if line_lower.lstrip(" ").startswith("```"):
                    in_code_block = False
                current_section.append(lines[i])
            elif line_lower in TITLES_PARAMETERS:
                if current_section:
                    if any(current_section):
                        sections.append(Section(Section.Type.MARKDOWN, current_section))
                    current_section = []
                section, i = self.read_parameters_section(lines, i + 1)
                if section:
                    sections.append(section)
            elif line_lower in TITLES_EXCEPTIONS:
                if current_section:
                    if any(current_section):
                        sections.append(Section(Section.Type.MARKDOWN, current_section))
                    current_section = []
                section, i = self.read_exceptions_section(lines, i + 1)
                if section:
                    sections.append(section)
            elif line_lower in TITLES_RETURN:
                if current_section:
                    if any(current_section):
                        sections.append(Section(Section.Type.MARKDOWN, current_section))
                    current_section = []
                section, i = self.read_return_section(lines, i + 1)
                if section:
                    sections.append(section)
            elif line_lower.lstrip(" ").startswith("```"):
                in_code_block = True
                current_section.append(lines[i])
            else:
                if admonitions and not in_code_block and i + 1 < len(lines):
                    match = RE_GOOGLE_STYLE_ADMONITION.match(lines[i])
                    if match:
                        groups = match.groupdict()
                        indent = groups["indent"]
                        if lines[i + 1].startswith(indent + " " * 4):
                            lines[i] = f"{indent}!!! {groups['type'].lower()}"
                            if groups["title"]:
                                lines[i] += f' "{groups["title"]}"'
                current_section.append(lines[i])
            i += 1

        if current_section:
            sections.append(Section(Section.Type.MARKDOWN, current_section))

        return sections

    @staticmethod
    def read_block_items(lines: List[str], start_index: int) -> Tuple[List[str], int]:
        """
        Parse an indented block as a list of items.

        Each item is indented by four spaces. Every line indented with more than five spaces are concatenated
        back into the previous line.

        Arguments:
            lines: The block lines.
            start_index: The line number to start at.

        Returns:
            A tuple containing the list of concatenated lines and the index at which to continue parsing.
        """
        i = start_index
        block: List[str] = []
        prefix = " "
        while i < len(lines) and (lines[i].startswith("    ") or not lines[i].strip()):
            if block and lines[i].startswith("      "):
                block[-1] += prefix + lines[i].lstrip(" ")
                prefix = " "
            elif block and not lines[i].strip():
                block[-1] += "\n\n"
                prefix = ""
            else:
                block.append(lines[i])
            i += 1
        cleaned_up_block = []
        for line in block:
            stripped = line.strip()
            if stripped:
                cleaned_up_block.append(stripped)
        return cleaned_up_block, i - 1

    @staticmethod
    def read_block(lines: List[str], start_index: int) -> Tuple[List[str], int]:
        """
        Parse an indented block.

        Arguments:
            lines: The block lines.
            start_index: The line number to start at.

        Returns:
            A tuple containing the list of lines and the index at which to continue parsing.
        """
        i = start_index
        block = []
        while i < len(lines) and (lines[i].startswith("    ") or not lines[i].strip()):
            block.append(lines[i])
            i += 1
        return block, i - 1

    def read_parameters_section(self, lines: List[str], start_index: int) -> Tuple[Optional[Section], int]:
        """
        Parse a "parameters" section.

        Arguments:
            lines: The parameters block lines.
            start_index: The line number to start at.

        Returns:
            A tuple containing a `Section` (or `None`) and the index at which to continue parsing.
        """
        parameters = []
        type_: Any
        block, i = self.read_block_items(lines, start_index)
        for param_line in block:
            try:
                name_with_type, description = param_line.lstrip(" ").split(":", 1)
            except ValueError:
                self.parsing_errors.append(f"{self.path}: Failed to get 'name: description' pair from '{param_line}'")
                continue

            if " " in name_with_type:
                name, type_ = name_with_type.split(" ", 1)
                type_ = type_.strip("()")
                if type_.endswith(", optional"):
                    type_ = type_[:-10]
            else:
                name = name_with_type
                type_ = empty

            default = empty
            annotation = type_
            kind = None

            try:
                signature_param = self.signature.parameters[name]  # type: ignore
            except (AttributeError, KeyError):
                self.parsing_errors.append(f"{self.path}: No type annotation for parameter '{name}'")
            else:
                if signature_param.annotation is not empty:
                    annotation = signature_param.annotation
                if signature_param.default is not empty:
                    default = signature_param.default
                kind = signature_param.kind

            parameters.append(
                Parameter(
                    name=name, annotation=annotation, description=description.lstrip(" "), default=default, kind=kind,
                )
            )

        if parameters:
            return Section(Section.Type.PARAMETERS, parameters), i

        self.parsing_errors.append(f"{self.path}: Empty parameters section at line {start_index}")
        return None, i

    def read_exceptions_section(self, lines: List[str], start_index: int) -> Tuple[Optional[Section], int]:
        """
        Parse an "exceptions" section.

        Arguments:
            lines: The exceptions block lines.
            start_index: The line number to start at.

        Returns:
            A tuple containing a `Section` (or `None`) and the index at which to continue parsing.
        """
        exceptions = []
        block, i = self.read_block_items(lines, start_index)
        for exception_line in block:
            annotation, description = exception_line.split(": ")
            exceptions.append(AnnotatedObject(annotation, description.lstrip(" ")))
        if exceptions:
            return Section(Section.Type.EXCEPTIONS, exceptions), i

        self.parsing_errors.append(f"{self.path}: Empty exceptions section at line {start_index}")
        return None, i

    def read_return_section(self, lines: List[str], start_index: int) -> Tuple[Optional[Section], int]:
        """
        Parse an "returns" section.

        Arguments:
            lines: The return block lines.
            start_index: The line number to start at.

        Returns:
            A tuple containing a `Section` (or `None`) and the index at which to continue parsing.
        """
        block, i = self.read_block(lines, start_index)
        if self.signature:
            annotation = self.signature.return_annotation
        else:
            annotation = self.return_type

        if annotation is empty:
            if not block:
                self.parsing_errors.append(f"{self.path}: No return type annotation")
            else:
                try:
                    type_, first_line = block[0].split(":", 1)
                except ValueError:
                    self.parsing_errors.append(f"{self.path}: No type in return description")
                else:
                    annotation = type_.lstrip(" ")
                    block[0] = first_line.lstrip(" ")

        description = dedent("\n".join(block))
        if annotation is empty and not description:
            self.parsing_errors.append(f"{self.path}: Empty return section at line {start_index}")
            return None, i

        return Section(Section.Type.RETURN, AnnotatedObject(annotation, description)), i


def rebuild_optional(matched_group: str) -> str:
    brackets_level = 0
    for char in matched_group:
        if char == "," and brackets_level == 0:
            return f"Union[{matched_group}]"
        elif char == "[":
            brackets_level += 1
        elif char == "]":
            brackets_level -= 1
    return matched_group


def annotation_to_string(annotation: Any):
    if annotation is empty:
        return ""

    if inspect.isclass(annotation) and not isinstance(annotation, GenericMeta):
        s = annotation.__name__
    else:
        s = str(annotation).replace("typing.", "")

    s = RE_FORWARD_REF.sub(lambda match: match.group(1), s)
    s = RE_OPTIONAL.sub(lambda match: f"Optional[{rebuild_optional(match.group(1))}]", s)

    return s


def parse(
    path: str,
    docstring: str,
    signature: Optional[inspect.Signature] = None,
    return_type: Optional[Any] = empty,
    admonitions: bool = True,
):
    parser = DocstringParser(path, docstring, signature, return_type)
    return parser.parse(admonitions), parser.parsing_errors
