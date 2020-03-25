"""
While recursing on a class inheriting from `typing.NamedTuple`, the class' `__dict__` returns items
that are identified as properties.

When trying to get the signature of these properties' `fget` methods,
`inspect` raises a `ValueError: callable operator.itemgetter(0) is not supported by signature` error.

Instead of failing, we simply set the signature to `None`.

References:

- Test case: [tests.test_loader.test_inheriting_typing_NamedTuple][].
- Issue reported at [pawamoy/pytkdocs#15](https://github.com/pawamoy/pytkdocs/issues/15).
- Fixed by commit [67cee40](https://github.com/pawamoy/pytkdocs/commit/67cee406baccc8789566ed72ee040728c934f49d).
- See other "inheriting" test cases.
"""

from typing import NamedTuple


class MyNamedTupleType(NamedTuple):
    """My custom named tuple type docstring."""

    aaa: float
    bbb: float
    ccc: float
    ddd: float
