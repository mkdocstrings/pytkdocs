"""
Module docstring.

:var DESCRIBED_IN_MODULE_DOCSTRING: Described in module docstring.
:var DESCRIBED_AND_ANNOTATED_IN_MODULE_DOCSTRING: Described and annotated in module docstring.
:vartype DESCRIBED_AND_ANNOTATED_IN_MODULE_DOCSTRING: bool
:var DESCRIBED_IN_BOTH: Described in both.
:var DESCRIBED_AND_ANNOTATED_IN_BOTH: Described and annotated in both.
:vartype DESCRIBED_AND_ANNOTATED_IN_BOTH: bool
"""

from datetime import datetime
from typing import Optional, Tuple

from marshmallow import Schema, fields
from pydantic import BaseModel

NO_DOC_NO_TYPE = 0

NO_TYPE = 1
"""No type."""

NO_DOC_NO_VALUE: int

NO_VALUE: str
"""No value."""

NO_DOC: int = 2

FULL: int = 3
"""Full."""

DESCRIBED_IN_MODULE_DOCSTRING: bool = True
DESCRIBED_AND_ANNOTATED_IN_MODULE_DOCSTRING = True

DESCRIBED_IN_BOTH: bool = True
"""Described in both."""

DESCRIBED_AND_ANNOTATED_IN_BOTH: bool = True
"""Described and annotated in both."""

COMPLEX_TYPE: Optional[Tuple[int, str]] = None
"""Complex type."""


ATTRIBUTE_C1: "C"
"""Forward reference for type."""


ATTRIBUTE_C2: Optional["C"] = None
"""Optional forward reference for type."""


class C:
    """
    Class doctring.

    :cvar DESCRIBED_IN_CLASS_DOCSTRING: Described in class docstring.
    :cvar DESCRIBED_AND_ANNOTATED_IN_CLASS_DOCSTRING: Described and annotated in class docstring.
    :vartype DESCRIBED_AND_ANNOTATED_IN_CLASS_DOCSTRING: bool
    :cvar DESCRIBED_IN_BOTH: Described in both.
    :cvar DESCRIBED_AND_ANNOTATED_IN_BOTH: Described and annotated in both.
    :vartype DESCRIBED_AND_ANNOTATED_IN_BOTH: bool

    :var described_in_class_docstring: Described in class docstring.
    :var described_and_annotated_in_class_docstring: Described and annotated in class docstring.
    :vartype described_and_annotated_in_class_docstring: bool
    :var described_in_both: Described in both.
    :var described_and_annotated_in_both: Described and annotated in both.
    :vartype described_and_annotated_in_both: bool
    """

    IN_CLASS = 0
    """In class."""

    DESCRIBED_IN_CLASS_DOCSTRING: bool = True
    DESCRIBED_AND_ANNOTATED_IN_CLASS_DOCSTRING = True

    DESCRIBED_IN_BOTH: bool = True
    """Described in both."""

    DESCRIBED_AND_ANNOTATED_IN_BOTH: bool = True
    """Described and annotated in both."""

    both_class_and_instance_attribute: Optional[bool] = None

    def __init__(self):
        self.in_init = True
        """In init."""

        self.annotated_in_init: bool = True
        """Annotated in init."""

        self.described_in_class_docstring: bool = True
        self.described_and_annotated_in_class_docstring = True

        self.described_in_both: bool = True
        """Described in both."""

        self.described_and_annotated_in_both: bool = True
        """Described and annotated in both."""

        non_attribute: bool = True
        """Non attribute."""

        if not self.both_class_and_instance_attribute:
            self.both_class_and_instance_attribute = True


class D:
    def __init__(self):
        """
        Init doctring.

        :var described_in_class_docstring: Described in class docstring.
        :var described_and_annotated_in_class_docstring: Described and annotated in class docstring.
        :vartype described_and_annotated_in_class_docstring: bool
        :var described_in_both: Described in both.
        :var described_and_annotated_in_both: Described and annotated in both.
        :vartype described_and_annotated_in_both: bool
        """
        self.in_init = True
        """In init."""

        self.annotated_in_init: bool = True
        """Annotated in init."""

        self.described_in_class_docstring: bool = True
        self.described_and_annotated_in_class_docstring = True

        self.described_in_both: bool = True
        """Described in both."""

        self.described_and_annotated_in_both: bool = True
        """Described and annotated in both."""

        non_attribute: bool = True
        """Non attribute."""

        if not self.both_class_and_instance_attribute:
            self.both_class_and_instance_attribute = True


class E:
    """
    Class doctring.

    :cvar DESCRIBED_IN_CLASS_DOCSTRING: Described in class docstring.
    :cvar DESCRIBED_AND_ANNOTATED_IN_CLASS_DOCSTRING: Described and annotated in class docstring.
    :vartype DESCRIBED_AND_ANNOTATED_IN_CLASS_DOCSTRING: bool
    :cvar DESCRIBED_IN_BOTH: Described in both.
    :cvar DESCRIBED_AND_ANNOTATED_IN_BOTH: Described and annotated in both.
    :vartype DESCRIBED_AND_ANNOTATED_IN_BOTH: bool

    :var described_in_class_and_init_docstring: Described in class and init docstring.
    :var described_and_annotated_in_class_and_init_docstring: Described and annotated in class and init docstring.
    :vartype described_and_annotated_in_class_and_init_docstring: bool
    :var described_everywhere: Described everywhere.
    :var described_and_annotated_everywhere: Described and annotated everywhere.
    :vartype described_and_annotated_everywhere: bool
    """

    IN_CLASS = 0
    """In class."""

    DESCRIBED_IN_CLASS_DOCSTRING: bool = True
    DESCRIBED_AND_ANNOTATED_IN_CLASS_DOCSTRING = True

    DESCRIBED_IN_BOTH: bool = True
    """Described in both."""

    DESCRIBED_AND_ANNOTATED_IN_BOTH: bool = True
    """Described and annotated in both."""

    both_class_and_instance_attribute: Optional[bool] = None

    def __init__(self):
        """
        Init doctring.

        :var described_in_class_and_init_docstring: Described in class and init docstring.
        :var described_and_annotated_in_class_and_init_docstring: Described and annotated in class and init docstring.
        :vartype described_and_annotated_in_class_and_init_docstring: bool
        :var described_everywhere: Described everywhere.
        :var described_and_annotated_everywhere: Described and annotated everywhere.
        :vartype described_and_annotated_everywhere: bool
        """
        self.in_init = True
        """In init."""

        self.annotated_in_init: bool = True
        """Annotated in init."""

        self.described_in_class_and_init_docstring: bool = True
        self.described_and_annotated_in_class_and_init_docstring = True

        self.described_everywhere: bool = True
        """Described everywhere."""

        self.described_and_annotated_everywhere: bool = True
        """Described and annotated everywhere."""

        non_attribute: bool = True
        """Non attribute."""

        non_attribute2 = True
        """Non attribute 2."""

        if not self.both_class_and_instance_attribute:
            self.both_class_and_instance_attribute = True

        d = D()
        d.non_self_attribute = 0
        """Non self attribute."""

        self.d = d
        self.d.non_self_attribute2 = 0
        """Non self attribute 2."""

        c = C()
        c.non_self_attribute: int = 0
        """Non self attribute."""

        self.c = c
        self.c.non_self_attribute2: int = 0
        """Non self attribute 2."""


if True:
    IN_IF: bytes = b""
    """In if."""

    ANNOTATED_IN_IF: str = ""
    """Annotated in if."""
else:
    IN_ELSE: list = []
    """In else."""

try:
    IN_TRY: int = 1000
    """In try."""
except:  # noqa
    IN_EXCEPT: float = 9000.0
    """In except."""
else:
    IN_TRY_ELSE: str = "-1"
    """In try else."""
finally:
    IN_FINALLY: bool = bool(-9000)
    """In finally."""


class Model(BaseModel):
    in_pydantic_model: int
    """In Pydantic model."""

    model_field: Optional[datetime] = None
    """A model field."""


class MarshmallowSchema(Schema):
    in_marshmallow_model: int
    """In Marshmallow model."""

    model_field: fields.Str = fields.Str()
    """A model field."""


OK, WARNING, CRITICAL, UNKNOWN = 0, 0, 0, 0
