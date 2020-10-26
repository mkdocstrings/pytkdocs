class NotDefinedYet:
    @property
    def ha(self) -> "NotDefinedYet":
        """
        This property returns `self`.

        It's fun because you can call it like `obj.ha.ha.ha.ha.ha.ha...`.

        :return: self!
        """
        return self


class ClassInitFunction:
    def __init__(self, value: str, other=1) -> None:
        """
        Initialize instance.

        :param value: Value to store
        :param int other: Other value with default
        """
        self.value = value
        self.other = other


class ClassWithFunction:
    def thing(self, value: str, other=1) -> str:
        """
        Concatenate a integer after a string.

        :param value: Value to store
        :param int other: Other value with default
        :return: Concatenated result
        """
        return f"{value}{other}"
