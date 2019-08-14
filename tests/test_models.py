from datetime import datetime
from models import Base, Contest, Name
from slugify import slugify
from unittest import TestCase
from tests import TestMixin


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


class ContestTestCase(TestMixin, TestCase):

    def test_create(self):
        contest = create_contest(self.db)

        self.assertIsNotNone(contest.id)
        self.assertGreaterEqual(Contest.query.count(), 1)

    def test_name_slug(self):
        contest_name = 'Sorteio de uma paçoquita'
        contest = create_contest(self.db, contest_name, 'Sorteio de uma caixa de paçoquita')

        self.assertEqual(contest.slug, slugify(contest_name, only_ascii=True))

    def test_key(self):
        contest = create_contest(self.db)

        self.assertIsInstance(contest.key, str)
        self.assertEqual(len(contest.key), 36)

    def test_raffle(self):
        contest = create_contest(self.db)
        names = create_names(self.db, contest)

        winner = contest.raffle()

        self.assertIn(str(winner), names)
        print(winner)
        self.assertTrue(winner.winner)

        self.assertIsNotNone(contest.held_in)
        print(contest.held_in)


class NameTestCase(TestMixin, TestCase):

    def test_create(self):

        contest = create_contest(self.db)
        name = create_name(self.db, 'Francisco', contest)

        self.assertIsNotNone(name.id)
        self.assertEqual(Name.query.count(), 1)
        self.assertEqual(Base.query.count(), Name.query.count() + Contest.query.count())
