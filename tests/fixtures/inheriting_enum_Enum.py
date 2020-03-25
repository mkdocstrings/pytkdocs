"""
While recursing on a class inheriting from `enum.Enum`, the class' `__dict__` returns private items
whose values are the `object` builtin for example.

The `object` builtin is a class, so `pytkdocs` is trying to recurse on it,
and tries to get its file path by first getting its module.

The `object` class' module is `builtins`, which does not have a `__file__` attribute,
so trying to access it generates an `AttributeError` error.

Instead of failing, we simply catch the error and set `file_path = ""`.

References:

- Test case: [tests.test_loader.test_inheriting_enum_Enum][].
- Issue reported on commit [5053f81](https://github.com/pawamoy/mkdocstrings/commit/5053f8142913f01358481e4801e5222d88482c35).
- Fixed by commit [48df6bc](https://github.com/pawamoy/pytkdocs/commit/48df6bc9cf878f3ce281fac6ccaf8fe1d4e89c84).
- See other "inheriting" test cases.
"""

import enum


class MyEnum(enum.Enum):
    """My custom enumeration docstring."""

    A = 0
    """Item A."""

    B = 1
    """Item B."""
