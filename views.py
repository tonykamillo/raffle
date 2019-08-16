from flask import current_app as app
from models import Contest, Name
from forms import ContestForm, NameForm
from serializers import ContestSchema, NameSchema
from app import db


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
    data = {'success': False, 'status': 500}
    serializer = ContestSchema()
    contest = Contest() if not pk else Contest.query.get(pk)

    if contest:
        form = ContestForm(csrf_enabled=False)

        if form.validate_on_submit():
            try:
                form.populate_obj(contest)
                db.session.add(contest)
                db.session.commit()
            except Exception as e:
                data.update(message=str(e))
            else:
                data.update(
                    success=True,
                    contest=serializer.dump(contest).data,
                    status=200 if pk else 201)

        else:
            data.update(message='Formulário preenchido de forma incorreta.', errors=form.errors, status=412)
    else:
        data.update(message='Sorteio não encontrado', status=404)
    return data, data.get('status')


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
    data = {'success': False, 'status': 500}
    serializer = NameSchema()
    name = Name() if not pk else Name.query.get(pk)

    if name:
        form = NameForm(csrf_enabled=False)

        if form.validate_on_submit():
            try:
                form.populate_obj(name)
                db.session.add(name)
                db.session.commit()
            except Exception as e:
                data.update(message=str(e))
            else:
                data.update(
                    success=True,
                    name=serializer.dump(name).data,
                    status=200 if pk else 201)

        else:
            data.update(message='Formulário preenchido de forma incorreta.', errors=form.errors, status=412)
    else:
        data.update(message='Nome não encontrado', status=404)
    return data, data.get('status')
