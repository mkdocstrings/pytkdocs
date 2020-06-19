from marshmallow import Schema, fields


class Person(Schema):
    """Simple Marshmallow Model for a person's information"""

    name: fields.Str = fields.Str(description="The person's name", required=True)
    age: fields.Int = fields.Int(description="The person's age which must be at minimum 18")
