import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Can(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'info'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    loc = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    fill = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    days = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

