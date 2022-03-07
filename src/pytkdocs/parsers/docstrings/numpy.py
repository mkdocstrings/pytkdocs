"""This module defines functions and classes to parse docstrings into structured data."""
import re
from typing import List, Optional, Pattern

from docstring_parser import parse
from docstring_parser.common import Docstring, DocstringMeta

from pytkdocs.parsers.docstrings.base import AnnotatedObject, Attribute, Parameter, Parser, Section, empty

RE_DOCTEST_BLANKLINE: Pattern = re.compile(r"^\s*<BLANKLINE>\s*$")
"""Regular expression to match lines of the form `<BLANKLINE>`."""
RE_DOCTEST_FLAGS: Pattern = re.compile(r"(\s*#\s*doctest:.+)$")
"""Regular expression to match lines containing doctest flags of the form `# doctest: +FLAG`."""


class Numpy(Parser):
    """A Numpy-style docstrings parser."""

    def __init__(self, trim_doctest_flags: bool = True) -> None:
        """
        Initialize the objects.

        Arguments:
            trim_doctest_flags: Whether to remove doctest flags.
        """
        super().__init__()
        self.trim_doctest_flags = trim_doctest_flags
        self.section_reader = {
            Section.Type.PARAMETERS: self.read_parameters_section,
            Section.Type.EXCEPTIONS: self.read_exceptions_section,
            Section.Type.EXAMPLES: self.read_examples_section,
            Section.Type.ATTRIBUTES: self.read_attributes_section,
            Section.Type.RETURN: self.read_return_section,
        }

    def parse_sections(self, docstring: str) -> List[Section]:  # noqa: D102
        if "signature" not in self.context:
            self.context["signature"] = getattr(self.context["obj"], "signature", None)
        if "annotation" not in self.context:
            self.context["annotation"] = getattr(self.context["obj"], "type", empty)
        if "attributes" not in self.context:
            self.context["attributes"] = {}

        docstring_obj = parse(docstring)
        description_all = (
            none_str_cast(docstring_obj.short_description) + "\n\n" + none_str_cast(docstring_obj.long_description)
        ).strip()
        sections = [Section(Section.Type.MARKDOWN, description_all)] if description_all else []
        sections_other = [
            reader(docstring_obj)  # type: ignore
            if sec == Section.Type.RETURN
            else reader(docstring, docstring_obj)  # type: ignore
            for (sec, reader) in self.section_reader.items()
        ]
        sections.extend([sec for sec in sections_other if sec])
        return sections

    def read_parameters_section(
        self,
        docstring: str,
        docstring_obj: Docstring,
    ) -> Optional[Section]:
        """
        Parse a "parameters" section.

        Arguments:
            docstring: The raw docstring.
            docstring_obj: Docstring object parsed by docstring_parser.

        Returns:
            A `Section` object (or `None` if section is empty).
        """
        parameters = []

        docstring_params = [p for p in docstring_obj.params if p.args[0] == "param"]

        for param in docstring_params:
            name = param.arg_name
            kind = None
            type_name = param.type_name
            default = param.default or empty
            try:
                signature_param = self.context["signature"].parameters[name.lstrip("*")]
            except (AttributeError, KeyError):
                self.error(f"No type annotation for parameter '{name}'")
            else:
                if signature_param.annotation is not empty:
                    type_name = signature_param.annotation
                if signature_param.default is not empty:
                    default = signature_param.default
                kind = signature_param.kind

            description = param.description or ""
            if not description:
                self.error(f"No description for parameter '{name}'")

            parameters.append(
                Parameter(
                    name=param.arg_name,
                    annotation=type_name,
                    description=description,
                    default=default,
                    kind=kind,
                )
            )

        if parameters:
            return Section(Section.Type.PARAMETERS, parameters)
        if re.search("Parameters\n", docstring):
            self.error("Empty parameter section")
        return None

    def read_attributes_section(
        self,
        docstring: str,
        docstring_obj: Docstring,
    ) -> Optional[Section]:
        """
        Parse an "attributes" section.

        Arguments:
            docstring: The raw docstring.
            docstring_obj: Docstring object parsed by docstring_parser.

        Returns:
            A `Section` object (or `None` if section is empty).
        """
        attributes = []
        docstring_attributes = [p for p in docstring_obj.params if p.args[0] == "attribute"]

        for attr in docstring_attributes:
            description = attr.description or ""
            if not description:
                self.error(f"No description for attribute '{attr.arg_name}'")
            attributes.append(
                Attribute(
                    name=attr.arg_name,
                    annotation=attr.type_name,
                    description=attr.description,
                )
            )

        if attributes:
            return Section(Section.Type.ATTRIBUTES, attributes)
        if re.search("Attributes\n", docstring):
            self.error("Empty attributes section")
        return None

    def read_exceptions_section(
        self,
        docstring: str,
        docstring_obj: Docstring,
    ) -> Optional[Section]:
        """
        Parse an "exceptions" section.

        Arguments:
            docstring: The raw docstring.
            docstring_obj: Docstring object parsed by docstring_parser.

        Returns:
            A `Section` object (or `None` if section is empty).
        """
        exceptions = []
        except_obj = docstring_obj.raises

        for exception in except_obj:
            description = exception.description or ""
            if not description:
                self.error(f"No description for exception '{exception.type_name}'")
            exceptions.append(AnnotatedObject(exception.type_name, description))

        if exceptions:
            return Section(Section.Type.EXCEPTIONS, exceptions)
        if re.search("Raises\n", docstring):
            self.error("Empty exceptions section")
        return None

    def read_return_section(
        self,
        docstring_obj: Docstring,
    ) -> Optional[Section]:
        """
        Parse a "returns" section.

        Arguments:
            docstring_obj: Docstring object parsed by docstring_parser.

        Returns:
            A `Section` object (or `None` if section is empty).
        """
        if docstring_obj.returns:
            return_obj = docstring_obj.returns

            if return_obj.description:
                description = return_obj.description
            else:
                self.error("Empty return description")
                description = ""

            if self.context["signature"]:
                annotation = self.context["signature"].return_annotation
            else:
                annotation = self.context["annotation"]

            if annotation is empty and return_obj.type_name:
                annotation = return_obj.type_name

            if not annotation:
                self.error("No return type annotation")
                annotation = ""

            if annotation or description:
                return Section(Section.Type.RETURN, AnnotatedObject(annotation, description))

        return None

    def read_examples_section(
        self,
        docstring: str,
        docstring_obj: Docstring,
    ) -> Optional[Section]:
        """
        Parse an "examples" section.

        Arguments:
            docstring: The raw docstring.
            docstring_obj: Docstring object parsed by docstring_parser.

        Returns:
            A `Section` object (or `None` if section is empty).
        """
        text = next(
            (
                meta.description
                for meta in docstring_obj.meta
                if isinstance(meta, DocstringMeta) and meta.args[0] == "examples"
            ),
            "",
        )

        sub_sections = []
        in_code_example = False
        in_code_block = False
        current_text: List[str] = []
        current_example: List[str] = []

        if text:
            for line in text.split("\n"):
                if is_empty_line(line):
                    if in_code_example:
                        if current_example:
                            sub_sections.append((Section.Type.EXAMPLES, "\n".join(current_example)))
                            current_example = []
                        in_code_example = False
                    else:
                        current_text.append(line)

                elif in_code_example:
                    if self.trim_doctest_flags:
                        line = RE_DOCTEST_FLAGS.sub("", line)
                        line = RE_DOCTEST_BLANKLINE.sub("", line)
                    current_example.append(line)

                elif line.startswith("```"):
                    in_code_block = not in_code_block
                    current_text.append(line)

                elif in_code_block:
                    current_text.append(line)

                elif line.startswith(">>>"):
                    if current_text:
                        sub_sections.append((Section.Type.MARKDOWN, "\n".join(current_text)))
                        current_text = []
                    in_code_example = True

                    if self.trim_doctest_flags:
                        line = RE_DOCTEST_FLAGS.sub("", line)
                    current_example.append(line)
                else:
                    current_text.append(line)

        if current_text:
            sub_sections.append((Section.Type.MARKDOWN, "\n".join(current_text)))
        elif current_example:
            sub_sections.append((Section.Type.EXAMPLES, "\n".join(current_example)))

        if sub_sections:
            return Section(Section.Type.EXAMPLES, sub_sections)

        if re.search("Examples\n", docstring):
            self.error("Empty examples section")
        return None


def is_empty_line(line: str) -> bool:
    """
    Tell if a line is empty.

    Arguments:
        line: The line to check.

    Returns:
        True if the line is empty or composed of blanks only, False otherwise.
    """
    return not line.strip()


def none_str_cast(string: Optional[str]):
    return string or ""
