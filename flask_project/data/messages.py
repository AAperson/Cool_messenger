import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'message'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    first_user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    second_user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)