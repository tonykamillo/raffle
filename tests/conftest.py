import os, pytest
from app import create_app


env = 'testing'
os.environ.setdefault('FLASK_ENV', env)

# @pytest.fixture
# def db():
#     return database


# @pytest.fixture
# def app():

#     env = 'testing'
#     os.environ.setdefault('FLASK_ENV', env)
#     app_instance = create_app(__name__)

#     print(app_instance.config)

#     with app_instance.app_context():
#         db.create_all()

#         yield app_instance

#         db.session.remove()
#         db.drop_all()


# @pytest.fixture
# def client(app, db):
#     """A test client for the app."""
#     with app.test_client() as client:
#         yield client
#         db.session.rollback()


@pytest.fixture
def app():
    app_instance = create_app(__name__)

    with app_instance.app_context():
        app_instance.db.create_all()
        yield app_instance
        app_instance.db.session.remove()
        app_instance.db.drop_all()


@pytest.fixture
def db(app):
    with app.app_context():
        yield app.db


# @pytest.fixture
# def client(app):
#     # app = create_app(__name__)
#     with app.app_context():
#         with app.test_client() as client:
#             yield client


@pytest.fixture
def client():
    app = create_app('%s -  test client' % __name__)

    with app.test_client() as client:
        with app.app_context():
            app.db.create_all()

            # app_instance.db.session.remove()
            # app_instance.db.drop_all()

        yield client

    # os.close(db_fd)
    # os.unlink(flaskr.app.config['DATABASE'])

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
