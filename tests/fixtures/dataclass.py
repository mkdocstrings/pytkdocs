from dataclasses import dataclass


@dataclass
class Person:
    """Simple dataclass for a person's information"""

    name: str
    age: int
    """Field description."""
