import functools


@functools.lru_cache(maxsize=1024)
def my_function(some_arg):
    """My docstring."""
    return some_arg


class A:
    @functools.lru_cache(maxsize=1024)
    def hello(self, name):
        """Hello!"""
        return f"Hello {name}!"
