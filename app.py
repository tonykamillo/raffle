import os, importlib, uuid
from datetime import datetime
from slugify import slugify as to_slug
from sqlalchemy import event
from flask import Flask
from flask_migrate import Migrate
from db_helpers import SQLAlchemy, JoinedInheritanceMixin

db = SQLAlchemy()


# class Base(JoinedInheritanceMixin, db.Model):
#     name = db.Column(db.String(100), nullable=False)
#     slug = db.Column(db.String(100), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
#     updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
#     deleted = db.Column(db.Boolean, default=False, nullable=False)


# @event.listens_for(Base.slug, 'set', retval=True)
# def slugify(target, value, old_value, initiator):
#     return to_slug(value)


# class Contest(Base):
#     key = db.Culumn(db.UUID, default=uuid.uuid4, index=True)
#     held_in = db.Column(db.DateTime)
#     description = db.Column(db.Text)


# class Name(Base):
#     winner = db.Column(db.Boolean, default=False, nullable=False, index=True)
#     contest_id = db.Column(db.UUID, db.ForeignKey('contest.id'))
#     contest = db.relationship('Contest', backref='names', foreign_keys=[contest_id])


def create_app(name=__name__, env=os.environ.get('FLASK_ENV') or 'development', config=None):

    envs = {
        'testing': 'config.TestingConfig',
        'development': 'config.DevelopmentConfig',
        'production': 'config.ProductionConfig'
    }

    if env != os.environ.get('FLASK_ENV'):
        os.environ.update({'FLASK_ENV': env})

    app = Flask(name)

    app.config.from_object(envs.get(env))
    if config:
        app.config.update(config)

    importlib.import_module('models')

    db.init_app(app)
    app.db = db

    Migrate(app, db, render_as_batch=True)

    return app
