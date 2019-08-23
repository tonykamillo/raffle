from app import ma
from marshmallow import fields
from models import Contest, Name


def fetch_object(obj, data):
    for k, v in data.items():
        if not k.startswith('_'):
            setattr(obj, k, v)


class ContestSchema(ma.ModelSchema):

    class Meta:
        model = Contest
        dump_only = ['id', 'slug']
        exclude = ['deleted', 'key']

    names = fields.Method('get_names', dump_only=True)

    def get_names(self, instance):
        names = instance.names.filter_by(deleted=False).all()
        return NameSchema(many=True, exclude=['contest']).dump(names).data


class ContestWithKeySchema(ContestSchema):
    class Meta(ContestSchema.Meta):
        exclude = ['deleted']


class NameSchema(ma.ModelSchema):

    class Meta:
        model = Name
        dump_only = ['id', 'slug', 'winner']

    contest_id = fields.String(load_only=True)
    contest = fields.Nested(ContestSchema, exclude=['names'], dump_only=True)
