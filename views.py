from flask import current_app as app, request
from models import Contest, Name
from pprint import pprint
from forms import ContestForm, NameForm
from serializers import ContestSchema, NameSchema, fetch_object
from marshmallow import ValidationError
from app import db, ma


def merge_obj(obj, obj2):
    pass


@app.route('/contests', methods=['GET'])
@app.route('/contests/<uuid:pk>', methods=['GET'])
def get_contests(pk=None):
    found = None
    serializer = None
    data = {'success': True, 'status': 200}
    query = Contest.query.filter_by()

    if pk:
        found = query.filter_by(id=pk).one()
        if not found:
            data.update(success=False, status=404, message='Sorteio não encontrado')
        serializer = ContestSchema()

    else:
        found = query.all()
        serializer = ContestSchema(many=True)

    data.update(found=serializer.dump(found).data)

    return data, data.get('status')


@app.route('/contests', methods=['POST'])
@app.route('/contests/<uuid:pk>', methods=['PUT'])
def add_or_update_contest(pk=None):

    json_data = request.get_json()
    if not json_data:
        return dict(success=False, message='Request must be json encoded'), 400

    serializer = ContestSchema()
    loaded_data = serializer.load(json_data)
    if loaded_data.errors:
        return dict(success=False, message='Validation error', errors=loaded_data.errors), 422

    contest = loaded_data.data

    if pk:
        contest = Contest.query.get(pk)
        if not contest:
            return dict(success=False, message='Contest not found'), 404
        else:
            fetch_object(contest, vars(loaded_data.data))

    try:
        db.session.add(contest)
        db.session.commit()
    except Exception as e:
        db.sesssion.rollback()
        return dict(success=False, message=str(e)), 500
    else:
        return dict(success=True, contest=serializer.dump(contest).data), 200 if pk else 201


@app.route('/contests/<uuid:pk>/raffle', methods=['PUT'])
def raffle(pk):
    data = {'success': False, 'status': 500}
    contest = Contest.query.get(pk)
    if contest:
        try:
            winner = contest.raffle()
            db.session.commit()
        except Exception as e:
            data.update(message=str(e))
        else:
            data.update(success=True, winner=NameSchema().dump(winner).data, status=200)
    else:
        data.update(status=404, message='Sorteio não encontrado.')
    db.session.commit()
    return data, data.get('status')


@app.route('/names', methods=['GET'])
@app.route('/names/<uuid:pk>', methods=['GET'])
@app.route('/contests/<uuid:contest>/names', methods=['GET'])
def get_names(pk=None, contest=None):
    data = {'success': True, 'status': 200}
    found = None
    serializer = None

    query = Name.query.filter_by()

    if pk:
        found = query.filter_by(id=pk).one()
        if not found:
            data.update(success=False, status=404, message='Nome não encontrado.')
        serializer = NameSchema()

    else:
        if contest:
            query = query.filter_by(contest_id=contest)

        found = query.all()
        serializer = NameSchema(many=True)

    data.update(found=serializer.dump(found).data)

    return data, data.get('status')


@app.route('/names', methods=['POST'])
@app.route('/names/<uuid:pk>', methods=['PUT'])
def add_or_update_name(pk=None):

    json_data = request.get_json()
    if not json_data:
        return dict(success=False, message='Request must be json encoded'), 400

    serializer = NameSchema()
    loaded_data = serializer.load(json_data)
    if loaded_data.errors:
        return dict(success=False, message='Validation error', errors=loaded_data.errors), 422

    name = loaded_data.data

    if pk:
        name = Name.query.get(pk)
        if not name:
            return dict(success=False, message='Name not found'), 404
        else:
            fetch_object(name, vars(loaded_data.data))

    try:
        db.session.add(name)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return dict(success=False, message=str(e)), 500
    else:
        return dict(success=True, name=serializer.dump(name).data), 200 if pk else 201
