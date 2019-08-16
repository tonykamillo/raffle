from flask import current_app
# from app import db


class TestMixin:

    def setUp(self):
        # print('Setting up %s tests' % self.__class__.__name__)
        self.app = current_app
        self.db = self.app.db
        self.db.create_all()

    def tearDown(self):
        # print('Tearing down %s tests' % self.__class__.__name__)
        self.db.session.remove()
        self.db.drop_all()
