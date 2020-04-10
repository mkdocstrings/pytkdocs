"""
This module defines function to serialize objects.

These functions simply take objects as parameters and return dictionaries that can be dumped by `json.dumps`.
"""


import inspect
import re
from typing import Any, Optional, Pattern

from .objects import Object, Source
from .parsers.docstrings import AnnotatedObject, Parameter, Section

try:
    from typing import GenericMeta  # python 3.6
except ImportError:
    # in 3.7, GenericMeta doesn't exist but we don't need it
    class GenericMeta(type):  # type: ignore
        pass


RE_OPTIONAL: Pattern = re.compile(r"Union\[(.+), NoneType\]")
"""Regular expression to match optional annotations of the form `Union[T, NoneType]`."""

RE_FORWARD_REF: Pattern = re.compile(r"_?ForwardRef\('([^']+)'\)")
"""Regular expression to match forward-reference annotations of the form `_ForwardRef('T')`."""


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
    if annotation is inspect.Signature.empty:
        return ""

    if inspect.isclass(annotation) and not isinstance(annotation, GenericMeta):
        s = annotation.__name__
    else:
        s = str(annotation).replace("typing.", "")

    s = RE_FORWARD_REF.sub(lambda match: match.group(1), s)
    s = RE_OPTIONAL.sub(lambda match: f"Optional[{rebuild_optional(match.group(1))}]", s)

    return s


def serialize_annotated_object(obj: AnnotatedObject) -> dict:
    """
    Serialize an instance of [`AnnotatedObject`][pytkdocs.parsers.docstrings.AnnotatedObject].

    Arguments:
        obj: The object to serialize.

    Returns:
        A JSON-serializable dictionary.
    """
    return dict(description=obj.description, annotation=annotation_to_string(obj.annotation))


def serialize_parameter(parameter: Parameter) -> dict:
    """
    Serialize an instance of [`Parameter`][pytkdocs.parsers.docstrings.Parameter].

    Arguments:
        parameter: The parameter to serialize.

    Returns:
        A JSON-serializable dictionary.
    """
    serialized = serialize_annotated_object(parameter)
    serialized.update(
        dict(
            name=parameter.name,
            kind=str(parameter.kind),
            default=parameter.default_string,
            is_optional=parameter.is_optional,
            is_required=parameter.is_required,
            is_args=parameter.is_args,
            is_kwargs=parameter.is_kwargs,
        )
    )
    return serialized


def serialize_signature_parameter(parameter: inspect.Parameter) -> dict:
    """
    Serialize an instance of `inspect.Parameter`.

    Arguments:
        parameter: The parameter to serialize.

    Returns:
        A JSON-serializable dictionary.
    """
    serialized = dict(kind=str(parameter.kind), name=parameter.name)
    if parameter.annotation is not parameter.empty:
        serialized["annotation"] = annotation_to_string(parameter.annotation)
    if parameter.default is not parameter.empty:
        serialized["default"] = repr(parameter.default)
    return serialized


def serialize_signature(signature: inspect.Signature) -> dict:
    """
    Serialize an instance of `inspect.Signature`.

    Arguments:
        signature: The signature to serialize.

    Returns:
        A JSON-serializable dictionary.
    """
    if signature is None:
        return {}
    serialized: dict = dict(
        parameters=[serialize_signature_parameter(value) for name, value in signature.parameters.items()]
    )
    if signature.return_annotation is not inspect.Signature.empty:
        serialized["return_annotation"] = annotation_to_string(signature.return_annotation)
    return serialized


def serialize_docstring_section(section: Section) -> dict:
    """
    Serialize an instance of `inspect.Signature`.

    Arguments:
        section: The section to serialize.

    Returns:
        A JSON-serializable dictionary.
    """
    serialized = dict(type=section.type)
    if section.type == section.Type.MARKDOWN:
        serialized.update(dict(value=section.value))
    elif section.type == section.Type.RETURN:
        serialized.update(dict(value=serialize_annotated_object(section.value)))
    elif section.type == section.Type.EXCEPTIONS:
        serialized.update(dict(value=[serialize_annotated_object(e) for e in section.value]))
    elif section.type == section.Type.PARAMETERS:
        serialized.update(dict(value=[serialize_parameter(p) for p in section.value]))
    return serialized


def serialize_source(source: Optional[Source]) -> dict:
    """
    Serialize an instance of [`Source`][pytkdocs.objects.Source].

    Arguments:
        source: The source to serialize.

    Returns:
        A JSON-serializable dictionary.
    """
    if source:
        return dict(code=source.code, line_start=source.line_start)
    return {}


def serialize_object(obj: Object) -> dict:
    """
    Serialize an instance of a subclass of [`Object`][pytkdocs.objects.Object].

    Arguments:
        obj: The object to serialize.

    Returns:
        A JSON-serializable dictionary.
    """
    serialized = dict(
        name=obj.name,
        path=obj.path,
        category=obj.category,
        file_path=obj.file_path,
        relative_file_path=obj.relative_file_path,
        properties=sorted(set(obj.properties + obj.name_properties)),
        parent_path=obj.parent_path,
        has_contents=obj.has_contents(),
        docstring=obj.docstring,
        docstring_sections=[serialize_docstring_section(s) for s in obj.docstring_sections],
        source=serialize_source(obj.source),
        children={child.path: serialize_object(child) for child in obj.children},
        attributes=[o.path for o in obj.attributes],
        methods=[o.path for o in obj.methods],
        functions=[o.path for o in obj.functions],
        modules=[o.path for o in obj.modules],
        classes=[o.path for o in obj.classes],
    )
    if hasattr(obj, "type"):
        serialized["type"] = annotation_to_string(obj.type)  # type: ignore
    if hasattr(obj, "signature"):
        serialized["signature"] = serialize_signature(obj.signature)  # type: ignore
    return serialized
