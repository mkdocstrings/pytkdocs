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

COMPLEX_TYPE: Optional[Tuple[int, str]] = None
"""Complex type."""


ATTRIBUTE_C1: "C"
"""Forward reference for type."""


ATTRIBUTE_C2: Optional["C"] = None
"""Optional forward reference for type."""


class C:
    IN_CLASS = 0
    """In class."""

    def __init__(self):
        self.in_init = True
        """In init."""


if True:
    IN_CONDITION = "hello"
    """In condition."""
else:
    NEVER_DEFINED = "never"
    """Never defined."""

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
