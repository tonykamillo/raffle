import uuid, random
from datetime import datetime
from sqlalchemy import event

from slugify import slugify as to_slug

from db_helpers import JoinedInheritanceMixin
from app import db


class Base(JoinedInheritanceMixin, db.Model):
    name = db.Column(db.String(100), nullable=False, index=True)
    slug = db.Column(db.String(100), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, index=True)
    deleted = db.Column(db.Boolean, default=False, nullable=False, index=True)

    def __str__(self):
        return '%s' % self.name


class Contest(Base):
    key = db.Column(db.UUID, default=uuid.uuid4, index=True)
    held_in = db.Column(db.DateTime, index=True)
    description = db.Column(db.Text)

    def raffle(self):
        names = self.names
        winner_name = random.choice(names)
        winner_name.winner = True
        db.session.add(winner_name)
        self.held_in = datetime.now()
        db.session.add(self)
        return winner_name

    def __str__(self):
        return '%s - [%s]' % (self.name, self.key)


class Name(Base):
    winner = db.Column(db.Boolean, default=False, nullable=False, index=True)
    contest_id = db.Column(db.UUID, db.ForeignKey('contest.id'))
    contest = db.relationship('Contest', backref='names', foreign_keys=[contest_id])

    def __repr__(self):
        return '%s' % self.name


@event.listens_for(Base, 'before_insert')
@event.listens_for(Base, 'before_update')
@event.listens_for(Contest, 'before_insert')
@event.listens_for(Contest, 'before_update')
@event.listens_for(Name, 'before_insert')
@event.listens_for(Name, 'before_update')
def slugify(mapper, connection, target):
    slug = to_slug(target.name, only_ascii=True)
    if slug != target.slug:
        target.slug = slug
