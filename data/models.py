import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .db_session import SqlAlchemyBase


users_to_books = sqlalchemy.Table(
    'users_to_books',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('book_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('books.id'))
)

users_to_words = sqlalchemy.Table(
    'users_to_words',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('word_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('words.id')),
    sqlalchemy.Column('word_level', sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column('next_date_training', sqlalchemy.DateTime, default=datetime.datetime.now)
)


class Users(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False, unique=True)
    email = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False, unique=True)
    tg_username = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    creation_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    books = orm.relationship("Books", secondary=users_to_books, back_populates='users')
    words = orm.relationship("Words", secondary=users_to_words, back_populates='users')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Books(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "books"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    author = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)
    creator_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    pages = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    difficult_level = sqlalchemy.Column(sqlalchemy.VARCHAR(6), nullable=False)

    users = orm.relationship("Users", secondary=users_to_books, back_populates='books')


class Words(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "words"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    word_tat = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False, unique=True)
    word_ru = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False, unique=True)

    users = orm.relationship("Users", secondary=users_to_words, back_populates='words')


class Questions(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "questions"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False, unique=True)


class Possible_answers(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "possibles_answers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    question_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('questions.id'), nullable=False)
    answer = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)
    is_correct_answer = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)