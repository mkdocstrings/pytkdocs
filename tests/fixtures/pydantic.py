from pydantic import BaseModel, Field


class Person(BaseModel):
    """Simple Pydantic Model for a person's information"""

    name: str = Field("PersonA", description="The person's name")
    age: int = Field(18, description="The person's age which must be at minimum 18")
