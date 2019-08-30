from slugify import slugify
from pprint import pprint


def create_contest(client, data):
    return client.post('/contests/', json=data)


def is_json_response(response):
    json_data = response.get_json()
    assert json_data is not None
    return json_data


def test_create_contest(client):
    data = {
        'name': 'Sorteio de paçoquita',
        'description': 'Sorteio de uma caixa de paçoquita'
    }

    r = create_contest(client, data)
    json_data = is_json_response(r)
    contest = json_data.get('data')
    assert r.status_code == 201
    assert contest['name'] == data['name']
    assert contest['description'] == data['description']
    assert contest['key'] is not None
    assert contest['held_in'] is None
    assert contest['slug'] == slugify(data['name'], only_ascii=True)


def test_get_contests(client):
    contest = create_contest(client, {'name': 'Sorteio de picolé'}).get_json().get('data')

    r = client.get('/contests/')

    json_data = is_json_response(r)
    assert r.status_code == 200
    found = json_data.get('found')
    assert len(found) == 1
    assert found[0].get('id') == contest.get('id')


def create_name(client, data):
    return client.post('/names/', json=data)


def create_names(client, names, contest):
    return [create_name(client, name, contest).get_json() for name in names]


def test_create_name(client):
    contest = create_contest(
        client, {'name': 'Sorteio de percata'}
    ).get_json().get('data')
    data = {'name': 'Tião Kilambi', 'contest_id': contest.get('id')}

    r = create_name(client, data)
    json_data = is_json_response(r)
    name = json_data.get('data')
    assert r.status_code == 201
    assert name['name'] == data['name']
    assert name['contest']['id'] == data['contest_id']
    assert name['winner'] is False
    assert name['slug'] == slugify(data['name'], only_ascii=True)
