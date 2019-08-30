import os, pytest
from app import create_app, db as _db


env = 'testing'
os.environ.setdefault('FLASK_ENV', env)
app_instance = create_app(__name__)


@pytest.fixture
def app():
    with app_instance.app_context():
        app_instance.db.create_all()
        yield app_instance
        app_instance.db.session.remove()
        app_instance.db.drop_all()


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def client(app):
    return app.test_client()
