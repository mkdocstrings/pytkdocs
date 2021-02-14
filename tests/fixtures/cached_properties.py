try:
    from functools import cached_property
except ImportError:
    from cached_property import cached_property


class C:
    @cached_property
    def aaa(self):
        """aaa"""
