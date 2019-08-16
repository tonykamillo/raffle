from app import ma
from marshmallow import fields
from models import Contest, Name


class ContestSchema(ma.ModelSchema):
    class Meta:
        model = Contest
    names = fields.Nested('NameSchema', many=True)


class NameSchema(ma.ModelSchema):
    class Meta:
        model = Name
    contest = fields.Nested(ContestSchema, exclude=['names'])
