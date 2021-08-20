from functools import lru_cache


@lru_cache()
def add(a, b):
    return a + b


# control
def sub(a, b):
    return a - b


# simulating a decorator that does not set __module__ properly
# on the wrapper object
del add.__module__
