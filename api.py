import re, datetime
from functools import wraps

from flask import current_app as app, request, abort, Response, url_for
from flask.views import MethodView
from marshmallow import ValidationError
from serializers import ContestSchema, ContestWithPrivateKeySchema, NameSchema, fetch_object
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
                parsed[k] = cast(v)
                break
    return parsed


def register_api(endpoint, api_name=None, pk='pk', pk_type='int'):

    class Decorator:
        def __init__(self, view_class):
            self.view_class = view_class

            api_indentifier = api_name or '%s' % self.view_class.__name__

            view_func = self.view_class.as_view(api_indentifier)

            app.add_url_rule(endpoint, defaults={pk: None}, view_func=view_func, methods=['GET'])
            app.add_url_rule(endpoint, view_func=view_func, methods=['POST'])
            app.add_url_rule('%s<%s:%s>' % (endpoint, pk_type, pk), view_func=view_func, methods=['GET', 'PUT', 'DELETE'])

        def __call__(self, *args, **kwargs):
            return self.view_class(*args, **kwargs)

    return Decorator


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


class CrudOperationsMixin:

    def use_serializer(self, name='default'):
        self.Serializer = self.serializers.get(name) or self.serializers.get('default')

    def get_serializer(self, **kwargs):
        if not getattr(self, 'Serializer', None):
            self.use_serializer('default')
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
        try:
            loaded_data = serializer.load(data)
            print('loaded data: %s' % loaded_data)
        except ValidationError as err:
            return dict(success=False, message='Validation error', errors=err.messages), 422
        else:
            return loaded_data

    def save(self, instance, is_update=False):
        try:
            db.session.add(instance)
            db.session.commit()
        except Exception as e:
            db.sesssion.rollback()
            return dict(success=False, message=str(e)), 500
        else:
            return dict(success=True, data=self.serialize(instance)), 200 if is_update else 201


class CrudApi(MethodView, CrudOperationsMixin):
    Model = None
    Serializer = None
    serializers = {}
    authorized = False

    def authorization(self, *args, **kwargs):
        return False

    def dispatch_request(self, *args, **kwargs):

        app.logger.info(kwargs)

        if not self.Serializer:
            self.use_serializer(request.method.lower())

        self.authorized = bool(self.authorization(*args, **kwargs))

        return super(CrudApi, self).dispatch_request(*args, **kwargs)

    # @cors()
    def get(self, pk=None):

        found = None
        query = self.get_query()
        if pk:
            found = self.Model.query.get(pk)
            if not found:
                return dict(success=False, message='%s not found' % self.Model.__name__), 404
        elif request.args:
            params = parse_args(dict(request.args))
            found = query.filter_by(**params).all()
        else:
            found = query.all()
        return dict(success=True, authorized=self.authorized, found=self.serialize(found))

    def post(self):

        data = self.validate_data()
        if isinstance(data, tuple) and not data[0].get('success'):
            return data
        return self.save(data)

    def put(self, pk):
        print('PUT method')

        data = self.validate_data()
        if isinstance(data, tuple) and not data[0].get('success'):
            return data

        instance = self.Model.query.get(pk)
        if not instance:
            return dict(success=False, message='%s not found' % self.Model.__name__), 404
        else:
            fetch_object(instance, vars(data))

        return self.save(instance, is_update=True)

    def delete(self, pk):
        instance = self.Model.query.get(pk)
        instance.deleted = True
        message = self.save(instance)
        if message[0].get('success'):
            return dict(success=True, message='The %s %s was deleted' % (self.Model.__name__, instance)), 200


def process_contest_authorization(*args, **kwargs):
    if request.method in ['PUT', 'DELETE']:
        key = request.headers.get('Authorization')
        query = Contest.query.filter_by(private_key=key)
        if query.count() == 0 or query.one().id != kwargs.get('pk'):
            abort(403)
        return query.one()

    if request.method in ['GET']:
        pubkey = request.args.get('key')
        privkey = request.headers.get('Authorization')

        params = {}
        if pubkey:
            params['public_key'] = pubkey
        elif privkey:
            params['private_key'] = privkey

        query = Contest.query.filter_by(**params)
        if query.count() == 1 and query.one().id != kwargs.get('pk'):
            return query.one()
    return False

@register_api('/contests/', pk_type='uuid')
class ContestApi(CrudApi):
    Model = Contest
    serializers = {
        'default': ContestSchema,
        'post': ContestWithPrivateKeySchema,
        'put': ContestWithPrivateKeySchema
    }

    def authorization(self, *args, **kwargs):
        return process_contest_authorization(*args, **kwargs)


@register_api('/names/', pk_type='uuid')
class NameApi(CrudApi):
    Model = Name
    Serializer = NameSchema

    def authorization(self, *args, **kwargs):
        if request.method in ['PUT', 'DELETE']:
            key = request.headers.get('Authorization')
            query = Contest.query.filter_by(private_key=key)
            name = Name.query.get(kwargs.get('pk'))
            if query.count() == 0 or query.one().id != name.contest.id:
                abort(403)
            return query.one()

        elif request.method in ['POST']:
            key = request.headers.get('Authorization')
            query = Contest.query.filter_by(public_key=key)
            if query.count() == 0:
                abort(403)
            return query.one()


@app.route('/contests/<uuid:pk>/join-link', endpoint='JoinApi', methods=['GET'])
def join(pk=None):

    contest = process_contest_authorization(pk=pk)

    if contest:
        return dict(success=True, link=url_for('ContestApi', pk=contest.id, key=contest.public_key))
    else:
        return dict(success=False, message='Contest not found.'), 404

@app.route('/contests/<uuid:pk>/raffle', endpoint='RaffleApi', methods=['PUT'])
def raffle(pk=None):

    contest = process_contest_authorization(pk=pk)

    if contest:
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
