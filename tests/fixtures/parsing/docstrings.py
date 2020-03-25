class NotDefinedYet:
    @property
    def ha(self) -> "NotDefinedYet":
        """
        This property returns `self`.

        It's fun because you can call it like `obj.ha.ha.ha.ha.ha.ha...`.

        Returns:
            self!
        """
        return self
