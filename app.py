import os, importlib
from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_wtf.csrf import CSRFProtect
from db_helpers import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()
csrf = CSRFProtect()


def create_app(name=__name__, config=None):

    envs = {
        'testing': 'config.TestingConfig',
        'development': 'config.DevelopmentConfig',
        'production': 'config.ProductionConfig'
    }

    env = os.environ.get('FLASK_ENV') or 'development'

    # print('creating app instance')
    app = Flask(name)
    app.config.update({'ENV': env})

    # print('setting config profile')
    app.config.from_object(envs.get(env))

    # print('Checking runtime config')
    if config:
        # print('Setting runtime config')
        app.config.update(config)

    # print('env: %s' % env)

    # print('loading models')
    importlib.import_module('models')

    # print('loading serializers')
    importlib.import_module('serializers')

    # print('initializing database')
    db.init_app(app)
    app.db = db

    # print('initializing serializer')
    ma.init_app(app)
    app.ma = ma

    csrf.init_app(app)

    # print('loading views')
    with app.app_context():
        importlib.import_module('views')

    # print('initialing database migrations tracking')
    Migrate(app, db, render_as_batch=True)
    # print(app.config)
    # print('\n')

    return app
