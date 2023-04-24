import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Img(SqlAlchemyBase):
    __tablename__ = 'imgs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    minetype = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
