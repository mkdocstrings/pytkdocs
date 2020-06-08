from pydantic import BaseModel as PydanticModel


class Base:
    V1 = "v1"
    """Variable 1."""

    def method1(self):
        """Method 1."""
        pass


class Child(Base):
    V2 = "v2"
    """Variable 2."""

    def method2(self):
        """Method 2."""
        pass


class BaseModel(PydanticModel):
    a: int


class ChildModel(BaseModel):
    b: str
