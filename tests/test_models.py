from models import Base, Contest, Name
from slugify import slugify


def add_and_commit(db, obj):
    db.session.add(obj)
    db.session.commit()


def create_contest(db, name='Sorteio de pamohna', description='Sorteio de 6 pamonhas doces com queijo'):
    contest = Contest(name=name, description=description)
    add_and_commit(db, contest)
    return contest


def create_name(db, name, contest):
    name = Name(name=name, contest=contest)
    add_and_commit(db, name)
    return name


def create_names(db, contest, names=['Mário', 'Maria', 'Juca', 'Elias', 'João', 'José', 'Marcos', 'Pedro']):
    for name in names:
        create_name(db, name, contest)

    return names


def test_create_contest(db):
    contest = create_contest(db)
    assert contest.id is not None
    assert Contest.query.count() >= 1


def test_name_slug(db):
    contest_name = 'Sorteio de uma paçoquita'
    contest = create_contest(db, contest_name, 'Sorteio de uma caixa de paçoquita')
    assert contest.slug == slugify(contest_name, only_ascii=True)


def test_key(db):
    contest = create_contest(db)

    assert isinstance(contest.key, str) is True
    assert len(contest.key) == 36


def test_raffle(db):
    contest = create_contest(db)
    names = create_names(db, contest)

    winner = contest.raffle()
    assert str(winner) in names
    assert winner.winner is True
    assert contest.held_in is not None


def test_create_name(db):
    # with app.app_context():
    contest = create_contest(db)
    name = create_name(db, 'Francisco', contest)

    assert name.id is not None
    assert Name.query.count() == 1
    assert Base.query.count() == Name.query.count() + Contest.query.count()
