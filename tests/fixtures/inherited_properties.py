class SuperClass:
    @property
    def read_only(self):
        """SuperClass.read_only docs"""
        return 0

    @property
    def mutable(self):
        """SuperClass.mutable getter docs"""
        return 0

    @mutable.setter
    def mutable(self, value):
        pass


class SubClass(SuperClass):
    @property
    def read_only(self):
        return 1

    @property
    def mutable(self):
        return 1

    @mutable.setter
    def mutable(self, value):
        pass
