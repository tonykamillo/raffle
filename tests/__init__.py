from flask import current_app
from app import db


class TestMixin:

    def setUp(self):
        # print('Setting up %s tests' % self.__class__.__name__)
        self.app = current_app
        self.db = db
        db.create_all()

    def tearDown(self):
        # print('Tearing down %s tests' % self.__class__.__name__)
        db.session.remove()
        db.drop_all()
