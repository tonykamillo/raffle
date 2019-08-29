from slugify import slugify
from pprint import pprint


CONTEST_DATA = {'name': 'Sorteio de paçoquita', 'description': 'Sorteio de uma caixa de paçoquita'}
NAMES = ['Juca Bolota', 'Xico Pinga', 'Zé Rasga Cueca', 'João da Ema']


def create_contest(client):
    return client.post('/contests/', json=CONTEST_DATA)


def is_json_response(response):
    json_data = response.get_json()
    assert json_data is not None
    return json_data


def test_create_contest(client):
    response = create_contest(client)
    json_data = is_json_response(response)
    contest = json_data.get('data')
    assert response.status_code == 201
    assert contest['name'] == CONTEST_DATA['name']
    assert contest['description'] == CONTEST_DATA['description']
    assert contest['key'] is not None
    assert contest['held_in'] is None
    assert contest['slug'] == slugify(CONTEST_DATA['name'], only_ascii=True)
    # assert 1 == 2


def test_get_contests(client):
    # create_response = client.get('/contests/')
    r = client.get('/contests/')
    pprint(r)
    pprint(vars(r))
    pprint(dir(r))
    # assert 1 == 2
    assert r.status_code == 200
    # json_data = is_json_response(response)
