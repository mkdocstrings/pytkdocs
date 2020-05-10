"""
Module docstring.

Attributes:
    DESCRIBED_IN_MODULE_DOCSTRING: Described in module docstring.
    DESCRIBED_AND_ANNOTATED_IN_MODULE_DOCSTRING (bool): Described and annotated in module docstring.
    DESCRIBED_IN_BOTH: Described in both.
    DESCRIBED_AND_ANNOTATED_IN_BOTH (bool): Described and annotated in both.
"""

from datetime import datetime
from typing import Optional, Tuple

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

    Attributes:
        DESCRIBED_IN_CLASS_DOCSTRING: Described in class docstring.
        DESCRIBED_AND_ANNOTATED_IN_CLASS_DOCSTRING (bool): Described and annotated in class docstring.
        DESCRIBED_IN_BOTH: Described in both.
        DESCRIBED_AND_ANNOTATED_IN_BOTH (bool): Described and annotated in both.

        described_in_class_docstring: Described in class docstring.
        described_and_annotated_in_class_docstring (bool): Described and annotated in class docstring.
        described_in_both: Described in both.
        described_and_annotated_in_both (bool): Described and annotated in both.
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

        Attributes:
            described_in_class_docstring: Described in class docstring.
            described_and_annotated_in_class_docstring (bool): Described and annotated in class docstring.
            described_in_both: Described in both.
            described_and_annotated_in_both (bool): Described and annotated in both.
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


class C:
    """
    Class doctring.

    Attributes:
        DESCRIBED_IN_CLASS_DOCSTRING: Described in class docstring.
        DESCRIBED_AND_ANNOTATED_IN_CLASS_DOCSTRING (bool): Described and annotated in class docstring.
        DESCRIBED_IN_BOTH: Described in both.
        DESCRIBED_AND_ANNOTATED_IN_BOTH (bool): Described and annotated in both.

        described_in_class_and_init_docstring: Described in class and init docstring.
        described_and_annotated_in_class_and_init_docstring (bool): Described and annotated in class and init docstring.
        described_everywhere: Described everywhere.
        described_and_annotated_everywhere (bool): Described and annotated everywhere.
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

        Attributes:
            described_in_class_and_init_docstring: Described in class and init docstring.
            described_and_annotated_in_class_and_init_docstring (bool): Described and annotated in class and init docstring.
            described_everywhere: Described everywhere.
            described_and_annotated_everywhere (bool): Described and annotated everywhere.
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

        if not self.both_class_and_instance_attribute:
            self.both_class_and_instance_attribute = True


if True:
    IN_IF = ""
    """In if."""

    ANNOTATED_IN_IF: str = ""
    """Annotated in if."""
else:
    IN_ELSE = ""
    """In else."""

try:
    IN_TRY = 1000
    """In try."""
except:  # noqa
    IN_EXCEPT = 9000
    """In except."""
else:
    IN_TRY_ELSE = -1
    """In try else."""
finally:
    IN_FINALLY = -9000
    """In finally."""


class Model(BaseModel):
    in_pydantic_model: int
    """In Pydantic model."""

    model_field: Optional[datetime] = None
    """A model field."""


def function():
    IN_FUNCTION: float = 0.1
    """In function."""

    return IN_FUNCTION
