"""
The module documentation.

Attributes:
    module_attribute: The module attribute docstring.
"""

class PyClass:
    """A Cython compiled Python class."""
    def method(self, arg, kwarg=''):
        """The method docstring."""
    
    @staticmethod
    def static_method():
        """The static method docstring."""
    
    @classmethod
    def class_method(self):
        """The class method docstring."""
    
    def __call__(self):
        """The special method docstring."""


cdef class CyClass:
    """
    A Cython class.

    Attributes:
        instance_attribute: The instance attribute docstring.
    """

    cdef readonly object instance_attribute

    def __call__(self):
        """The special method docstring."""

    def method(self, arg, kwarg=''):
        """The method docstring."""
    
    cpdef cpmethod(self, arg, kwarg=''):
        """The cpmethod docstring."""

def function(arg, kwarg=''):
    """The function docstring."""


cpdef cpfunction(arg, kwarg=''):
    """The cpfunction docstring."""


class PyClassInherit(CyClass):
    pass

module_attribute = object()
