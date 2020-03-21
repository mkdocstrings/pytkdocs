import inspect
import re
from textwrap import dedent
from typing import List

try:
    from typing import GenericMeta  # python 3.6
except ImportError:
    # in 3.7, GenericMeta doesn't exist but we don't need it
    class GenericMeta(type):
        pass


ADMONITIONS = {
    "note:": "note",
    "see also:": "seealso",
    "abstract:": "abstract",
    "summary:": "summary",
    "tldr:": "tldr",
    "info:": "info",
    "information:": "info",
    "todo:": "todo",
    "tip:": "tip",
    "hint:": "hint",
    "important:": "important",
    "success:": "success",
    "check:": "check",
    "done:": "done",
    "question:": "question",
    "help:": "help",
    "faq:": "faq",
    "warning:": "warning",
    "caution:": "caution",
    "attention:": "attention",
    "failure:": "failure",
    "fail:": "fail",
    "missing:": "missing",
    "danger:": "danger",
    "error:": "error",
    "bug:": "bug",
    "example:": "example",
    "snippet:": "snippet",
    "quote:": "quote",
    "cite:": "cite",
}

TITLES_PARAMETERS = ("args:", "arguments:", "params:", "parameters:")
TITLES_EXCEPTIONS = ("raise:", "raises:", "except:", "exceptions:")
TITLES_RETURN = ("return:", "returns:")

RE_OPTIONAL = re.compile(r"Union\[(.+), NoneType\]")
RE_FORWARD_REF = re.compile(r"_ForwardRef\('([^']+)'\)")

RE_GOOGLE_STYLE_ADMONITION = re.compile(r"^(?P<indent>\s*)(?P<type>[\w-]+):((?:\s+)(?P<title>.+))?$")


class AnnotatedObject:
    def __init__(self, annotation, description):
        self.annotation = annotation
        self.description = description

    @property
    def annotation_string(self):
        return annotation_to_string(self.annotation)


class Parameter(AnnotatedObject):
    def __init__(self, name, annotation, description, kind, default=inspect.Signature.empty):
        super().__init__(annotation, description)
        self.name = name
        self.kind = kind
        self.default = default

    @property
    def is_optional(self):
        return self.default is not inspect.Signature.empty

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
    def annotation_string(self):
        s = AnnotatedObject.annotation_string.fget(self)
        s = RE_FORWARD_REF.sub(lambda match: match.group(1), s)
        s = RE_OPTIONAL.sub(lambda match: f"Optional[{rebuild_optional(match.group(1))}]", s)
        return s

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
    class Type:
        MARKDOWN = "markdown"
        PARAMETERS = "parameters"
        EXCEPTIONS = "exceptions"
        RETURN = "return"

    def __init__(self, section_type, value):
        self.type = section_type
        self.value = value


class Docstring:
    def __init__(self, value, signature=None):
        self.original_value = value or ""
        self.signature = signature
        self.parsing_errors = []
        self.sections = self.parse()

    def parse(self, replace_admonitions: bool = True) -> List[Section]:
        """
        Parse a docstring!

        Note: This note has a title!
            to try notes.

        Trying some text in between.

        Parameters:
            replace_admonitions: Whether to replace block titles with their admonition equivalent.

        Returns:
            The docstring converted to a nice markdown text.

        And some final text:

        1. with an admonition
        2. in a bullet point

           Important: TITLE AS WELL!!!!!
               This is an important note!

           After-admonition text
        3. another bullet point.

        I'm done.
        """
        sections = []
        current_section = []

        in_code_block = False

        lines = self.original_value.split("\n")
        i = 0

        while i < len(lines):
            line_lower = lines[i].lower()
            if line_lower in TITLES_PARAMETERS:
                if current_section:
                    if any(current_section):
                        sections.append(Section(Section.Type.MARKDOWN, current_section))
                    current_section = []
                section, i = self.read_parameters_section(lines, i + 1)
                sections.append(section)
            elif line_lower in TITLES_EXCEPTIONS:
                if current_section:
                    if any(current_section):
                        sections.append(Section(Section.Type.MARKDOWN, current_section))
                    current_section = []
                section, i = self.read_exceptions_section(lines, i + 1)
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
                in_code_block = not in_code_block
                current_section.append(lines[i])
            else:
                if replace_admonitions and not in_code_block and i + 1 < len(lines):
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
    def read_block_items(lines, start_index):
        i = start_index
        block = []
        while i < len(lines) and lines[i].startswith("    "):
            if block and lines[i].startswith("      "):
                block[-1] += " " + lines[i].lstrip(" ")
            else:
                block.append(lines[i])
            i += 1
        return block, i - 1

    @staticmethod
    def read_block(lines, start_index):
        i = start_index
        block = []
        while i < len(lines) and (lines[i].startswith("    ") or lines[i] == ""):
            block.append(lines[i])
            i += 1
        return block, i - 1

    def read_parameters_section(self, lines, start_index):
        parameters = []
        block, i = self.read_block_items(lines, start_index)
        for param_line in block:
            try:
                name_with_type, description = param_line.lstrip(" ").split(":", 1)
            except Exception:
                self.parsing_errors.append(f"Failed to get 'name: description' pair from '{param_line}'")
                continue
            paren_index = name_with_type.find("(")
            if paren_index != -1:
                # name (type)
                name = name_with_type[0:paren_index].strip()
            else:
                # no type, just use name as-is
                name = name_with_type
            try:
                signature_param = self.signature.parameters[name]
            except (AttributeError, KeyError):
                self.parsing_errors.append(f"No type annotation for parameter '{name}'")
            else:
                parameters.append(
                    Parameter(
                        name=name,
                        annotation=signature_param.annotation,
                        description=description.lstrip(" "),
                        default=signature_param.default,
                        kind=signature_param.kind,
                    )
                )
        return Section(Section.Type.PARAMETERS, parameters), i

    def read_exceptions_section(self, lines, start_index):
        exceptions = []
        block, i = self.read_block_items(lines, start_index)
        for exception_line in block:
            annotation, description = exception_line.split(": ")
            exceptions.append(AnnotatedObject(annotation, description.lstrip(" ")))
        return Section(Section.Type.EXCEPTIONS, exceptions), i

    def read_return_section(self, lines, start_index):
        block, i = self.read_block(lines, start_index)
        description = dedent("\n".join(block))
        try:
            return_object = AnnotatedObject(self.signature.return_annotation, description)
        except AttributeError:
            self.parsing_errors.append(f"No return type annotation for return '{description}'")
            return None, i
        return Section(Section.Type.RETURN, return_object), i


def rebuild_optional(matched_group):
    brackets_level = 0
    for char in matched_group:
        if char == "," and brackets_level == 0:
            return f"Union[{matched_group}]"
        elif char == "[":
            brackets_level += 1
        elif char == "]":
            brackets_level -= 1
    return matched_group


def annotation_to_string(annotation):
    if annotation is inspect.Signature.empty:
        return ""
    if inspect.isclass(annotation) and not isinstance(annotation, GenericMeta):
        return annotation.__name__
    return str(annotation).replace("typing.", "")
