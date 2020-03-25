"""The module docstring."""

THE_ATTRIBUTE: int = 0
"""The attribute docstring."""


def the_function():
    """The function docstring."""


class TheClass:
    """The class docstring."""

    THE_ATTRIBUTE: float = 0.1
    """The attribute 0.1 docstring."""

    class TheNestedClass:
        """The nested class docstring."""

        THE_ATTRIBUTE: float = 0.2
        """The attribute 0.2 docstring."""

        class TheDoubleNestedClass:
            """The double nested class docstring."""

            THE_ATTRIBUTE: float = 0.3
            """The attribute 0.3 docstring."""

            def the_method(self):
                """The method3 docstring."""

        def the_method(self):
            """The method2 docstring."""

    def the_method(self):
        """The method1 docstring."""

    @staticmethod
    def the_static_method():
        """The static method docstring."""

    @classmethod
    def the_class_method(cls):
        """The class method docstring."""

    @property
    def the_property(self):
        """The property docstring."""

    @property
    def the_writable_property(self):
        """The writable property getter docstring."""

    @the_writable_property.setter
    def the_writable_property(self, value):
        """The writable property setter docstring."""
