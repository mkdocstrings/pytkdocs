import inspect


def serialize_annotated_object(obj):
    return dict(description=obj.description, annotation=obj.annotation_string)


def serialize_parameter(parameter):
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


def serialize_signature_parameter(parameter: inspect.Parameter):
    serialized = dict(kind=str(parameter.kind), name=parameter.name)
    if parameter.annotation is not parameter.empty:
        serialized["annotation"] = str(parameter.annotation)
    if parameter.default is not parameter.empty:
        serialized["default"] = repr(parameter.default)
    return serialized


def serialize_signature(signature: inspect.Signature) -> dict:
    if signature is None:
        return {}
    serialized = dict(parameters=[serialize_signature_parameter(value) for name, value in signature.parameters.items()])
    if signature.return_annotation is not inspect.Signature.empty:
        serialized["return_annotation"] = str(signature.return_annotation)
    return serialized


def serialize_docstring(docstring):
    return dict(
        original_value=docstring.original_value,
        signature=serialize_signature(docstring.signature),
        sections=[serialize_docstring_section(s) for s in docstring.sections],
    )


def serialize_docstring_section(section):
    serialized = dict(type=section.type)
    if section.type == section.Type.MARKDOWN:
        serialized.update(dict(value="\n".join(section.value)))
    elif section.type == section.Type.RETURN:
        serialized.update(dict(value=serialize_annotated_object(section.value)))
    elif section.type == section.Type.EXCEPTIONS:
        serialized.update(dict(value=[serialize_annotated_object(e) for e in section.value]))
    elif section.type == section.Type.PARAMETERS:
        serialized.update(dict(value=[serialize_parameter(p) for p in section.value]))
    return serialized


def serialize_object(obj):
    serialized = dict(
        name=obj.name,
        path=obj.path,
        category=obj.category,
        file_path=obj.file_path,
        relative_file_path=obj.relative_file_path,
        properties=sorted(set(obj.properties + obj.name_properties)),
        parent_path=obj.parent_path,
        has_contents=obj.has_contents,
        docstring=serialize_docstring(obj.docstring),
        source=obj.source,
        children={child.path: serialize_object(child) for child in obj.children},
        attributes=[o.path for o in obj.attributes],
        methods=[o.path for o in obj.methods],
        functions=[o.path for o in obj.functions],
        modules=[o.path for o in obj.modules],
        classes=[o.path for o in obj.classes],
    )
    if hasattr(obj, "type"):
        serialized["type"] = str(obj.type)
    return serialized
