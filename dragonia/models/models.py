from pyramid.security import Allow, Everyone

import sqlalchemy as sa
import sqlalchemy.orm as orm

import sqlalchemy.ext.declarative as declarative

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative.declarative_base()


def foreign_key_column(name, type_, target, nullable=False):
    """Construct a foreign key column for a table.

    ``name`` is the column name. Pass ``None`` to omit this arg in the
    ``Column`` call; i.e., in Declarative classes.

    ``type_`` is the column type.

    ``target`` is the other column this column references.

    ``nullable``: pass True to allow null values. The default is False
    (the opposite of SQLAlchemy's default, but useful for foreign keys).
    """
    fk = sa.ForeignKey(target)
    if name:
        return sa.Column(name, type_, fk, nullable=nullable)
    else:
        return sa.Column(type_, fk, nullable=nullable)


class User(Base):
    __tablename__ = 'users'
    uid = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Text, unique=True)
    password = sa.Column(sa.Text)

    @classmethod
    def all_users(cls):
        User = cls
        return q


class Group(Base):
    __tablename__ = 'groups'
    uid = sa.Column(sa.Integer, primary_key=True)
    group_name = sa.Column(sa.Text)
    user_uid = foreign_key_column(None, sa.Integer, "users.uid")


class MugloarGame(Base):
    __tablename__ = 'mugloar_games'
    uid = sa.Column(sa.Integer, primary_key=True)
    game_id = sa.Column(sa.Integer, unique=True)
    user_uid = foreign_key_column(None, sa.Integer, "users.uid")
    knight_agility = sa.Column(sa.Integer)
    knight_attack = sa.Column(sa.Integer)
    knight_endurance = sa.Column(sa.Integer)
    knight_armor = sa.Column(sa.Integer)
    weather = sa.Column(sa.Text)


class Battle(Base):
    __tablename__ = 'battles'
    uid =  sa.Column(sa.Integer, primary_key=True)
    mugloar_games_uid = foreign_key_column(None, sa.Integer, "mugloar_games.uid")
    result = sa.Column(sa.Text)
    result_text = sa.Column(sa.Text)
    dragon_name = sa.Column(sa.Text)
    dragon_wing_strength = sa.Column(sa.Integer)
    dragon_fire_breath = sa.Column(sa.Integer)
    dragon_claw_sharpness = sa.Column(sa.Integer)
    dragon_scale_thickness = sa.Column(sa.Integer)
