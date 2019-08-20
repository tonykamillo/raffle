from app import ma
from marshmallow import fields, post_load
from models import Contest, Name


def fetch_object(obj, data):
    for k, v in data.items():
        if not k.startswith('_'):
            setattr(obj, k, v)


class ContestSchema(ma.ModelSchema):

    class Meta:
        model = Contest
        dump_only = ['id', 'slug']

    names = fields.Nested('NameSchema', many=True)

    # @post_load
    # def make_object(self, data, **kwargs):
    #     print('%s: %s ' % (data, type(data)))
    #     print(kwargs)
    #     return data


class NameSchema(ma.ModelSchema):

    class Meta:
        model = Name
        dump_only = ['id', 'slug', 'winner']
        load_only = ['contest_id']

    contest_id = fields.String()
    contest = fields.Nested(ContestSchema, exclude=['names'], dump_only=True)

    # @post_load
    # def make_object(self, data, **kwargs):
    #     if data:
    #         return Name(**data)
