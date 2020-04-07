# See issue 65: https://github.com/pawamoy/mkdocstrings/issues/65


def method1():
    pass


def method2():
    pass


METHODS = {
    "method1": method1,
    "method2": method2,
}


class Class:
    pass


for name, method in METHODS.items():
    setattr(Class, name, method)
