import re, datetime
from flask import current_app as app, request
from flask.views import MethodView
from serializers import ContestSchema, ContestWithKeySchema, NameSchema, fetch_object
from models import Contest, Name
from app import db


def parse_args(args):
    patterns = [
        (r'False|True|None', eval),
        (r'[\d]{4}\-[\d]{2}\-[\d]{2}', datetime.date.fromisoformat),
        (r'[\d]{4}\-[\d]{2}\-[\d]{2}T[\d]{2}:[\d]{2}:[\w\+\.:]+', datetime.datetime.fromisoformat),
        (r'[\d]+\.[\d]*', float),
        (r'[\d]+', int),
        (r'.*', str)
    ]

    parsed = {}
    for k, v in args.items():
        for pattern, cast in patterns:
            match = re.match(pattern, v)
            if match:
                print(match)
                parsed[k] = cast(v)
                break
    return parsed


def register_api(view, endpoint, url, pk='pk', pk_type='int'):
    view_func = view.as_view(endpoint)

    app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET'])
    app.add_url_rule(url, view_func=view_func, methods=['POST'])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


class CrudOperationsMixin:

    def use_serializer(self, name='default'):
        self.Serializer = self.serializers.get(name) or self.serializers.get('default')

    def get_serializer(self, **kwargs):
        if not self.Serializer:
            self.use_serializer('default')
        print('serializer: %s' % self.Serializer)
        return self.Serializer(**kwargs)

    def serialize(self, obj):
        params = {}
        if not isinstance(obj, self.Model):
            params = {'many': True}
        return self.get_serializer(**params).dump(obj)

    def get_query(self):
        return self.Model.query.filter_by(deleted=False)

    def get_json(self):
        json_data = request.get_json()
        if not json_data:
            return dict(success=False, message='Request must be json encoded'), 400
        return json_data

    def validate_data(self):
        data = self.get_json()
        if isinstance(data, tuple):
            return data

        serializer = self.get_serializer()
        loaded_data = serializer.load(data)
        if loaded_data.errors:
            return dict(success=False, message='Validation error', errors=loaded_data.errors), 422
        return loaded_data.data

    def save(self, instance):
        try:
            db.session.add(instance)
            db.session.commit()
        except Exception as e:
            db.sesssion.rollback()
            return dict(success=False, message=str(e)), 500
        else:
            return dict(success=True, data=self.serialize(instance).data), 200 if instance.id else 201


class CrudApi(MethodView, CrudOperationsMixin):
    Model = None
    Serializer = None
    serializers = {}

    def get(self, pk=None):
        found = None
        query = self.get_query()
        if pk:
            found = query.get(pk)
            if not found:
                return dict(success=False, message='%s not found' % self.Model.__name__), 404
        elif request.args:
            params = parse_args(dict(request.args))
            found = query.filter_by(**params).all()
        else:
            found = query.all()
        return dict(success=True, found=self.serialize(found).data)

    def post(self):
        self.use_serializer('post')
        data = self.validate_data()
        if isinstance(data, tuple) and not data[0].get('success'):
            return data
        return self.save(data)

    def put(self, pk):
        self.use_serializer('put')

        data = self.validate_data()
        if isinstance(data, tuple) and not data[0].get('success'):
            return data

        instance = self.Model.query.get(pk)
        if not instance:
            return dict(success=False, message='%s not found' % self.Model.__name__), 404
        else:
            fetch_object(instance, vars(data))

        return self.save(instance)

    def delete(self, pk):
        instance = self.Model.query.get(pk)
        instance.deleted = True
        message = self.save(instance)
        if message[0].get('success'):
            return dict(success=True, message='The %s %s was deleted' % (self.Model.__name__, instance)), 200


class ContestApi(CrudApi):
    Model = Contest
    serializers = {
        'default': ContestSchema,
        'post': ContestWithKeySchema,
        'put': ContestWithKeySchema
    }

register_api(ContestApi, 'contest_api', '/contests/', pk_type='uuid')


class NameApi(CrudApi):
    Model = Name
    Serializer = NameSchema
register_api(NameApi, 'name_api', '/names/', pk_type='uuid')


@app.route('/contests/<uuid:pk>/raffle', endpoint='contest_api_ext', methods=['PUT'])
def raffle(pk):
    contest = Contest.query.get(pk)
    if contest:
        print(contest)
        try:
            winner = contest.raffle()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return dict(success=False, message=str(e)), 500
        else:
            return dict(success=True, winner=NameSchema().dump(winner).data)
    else:
        return dict(success=False, message='Contest not found.'), 404
