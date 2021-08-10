# -*- coding: utf-8 -*-
import flask_login

from apps.database.session import db, login_manager
from config import JsonConfig


def get_model(model):
    if JsonConfig.get_data('TESTING'):
        return model.test_model
    return model


class TestMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(120))


class TestTestModel(TestMixin, db.Model):
    __tablename__ = 'test_tests'


class TestModel(TestMixin, db.Model):
    __tablename__ = 'tests'

    test_model = TestTestModel


Test = get_model(TestModel)


class CinemaMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30))
    image_url = db.Column(db.Text())
    address = db.Column(db.String(50))
    detail_address = db.Column(db.String(30))


class TestCinemaModel(CinemaMixin, db.Model):
    __tablename__ = 'test_cinemas'


class CinemaModel(CinemaMixin, db.Model):
    __tablename__ = 'cinemas'

    test_model = TestCinemaModel


Cinema = get_model(CinemaModel)


class MovieMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    director = db.Column(db.String(20))
    description = db.Column(db.Text)
    poster_url = db.Column(db.Text)
    running_time = db.Column(db.Integer)
    age_rating = db.Column(db.Integer)


class TestMovieModel(MovieMixin, db.Model):
    __tablename__ = 'test_movies'

    showtimes = db.relationship('TestShowtimeModel', backref='movie', order_by='TestShowtimeModel.start_time')


class MovieModel(MovieMixin, db.Model):
    __tablename__ = 'movies'

    test_model = TestMovieModel

    showtimes = db.relationship('ShowtimeModel', backref='movie', order_by='ShowtimeModel.start_time')


Movie = get_model(MovieModel)


class ShowtimeMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)


class TestShowtimeModel(ShowtimeMixin, db.Model):
    __tablename__ = 'test_showtimes'

    cinema_id = db.Column(db.Integer, db.ForeignKey('test_cinemas.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('test_movies.id'))
    theater_id = db.Column(db.Integer, db.ForeignKey('test_theaters.id'))

    theater = db.relationship('TestTheaterModel', backref='showtimes')


class ShowtimeModel(ShowtimeMixin, db.Model):
    __tablename__ = 'showtimes'

    test_model = TestShowtimeModel

    cinema_id = db.Column(db.Integer, db.ForeignKey('cinemas.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    theater_id = db.Column(db.Integer, db.ForeignKey('theaters.id'))

    theater = db.relationship('TheaterModel', backref='showtimes')


Showtime = get_model(ShowtimeModel)


class TheaterTicketMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    x = db.Column(db.Integer())
    y = db.Column(db.Integer())


class TestTheaterTicketModel(TheaterTicketMixin, db.Model):
    __tablename__ = 'test_theater_tickets'

    showtime_id = db.Column(db.Integer(), db.ForeignKey('test_showtimes.id'))
    theater_id = db.Column(db.Integer(), db.ForeignKey('test_theaters.id'))


class TheaterTicketModel(TheaterTicketMixin, db.Model):
    __tablename__ = 'theater_tickets'

    test_model = TestTheaterTicketModel

    showtime_id = db.Column(db.Integer(), db.ForeignKey('showtimes.id'))
    theater_id = db.Column(db.Integer(), db.ForeignKey('theaters.id'))


TheaterTicket = get_model(TheaterTicketModel)


class TheaterMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(10))
    seat = db.Column(db.Integer())


class TestTheaterModel(TheaterMixin, db.Model):
    __tablename__ = 'test_theaters'

    cinema_id = db.Column(db.Integer(), db.ForeignKey('test_cinemas.id'))

    theater_tickets = db.relationship('TestTheaterTicketModel', backref='theater')


class TheaterModel(TheaterMixin, db.Model):
    __tablename__ = 'theaters'

    test_model = TestTheaterModel

    cinema_id = db.Column(db.Integer(), db.ForeignKey('cinemas.id'))

    theater_tickets = db.relationship('TheaterTicketModel', backref='theater')


Theater = get_model(TheaterModel)


class UserMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True)
    nickname = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(255))
    age = db.Column(db.Integer)


class TestUserModel(UserMixin, db.Model):
    __tablename__ = 'test_users'


class UserModel(UserMixin, flask_login.UserMixin, db.Model):
    __tablename__ = 'users'

    test_model = TestUserModel


User = get_model(UserModel)


@login_manager.user_loader
def member_loader(user_id):
    return User.query.filter(User.id == user_id).first()
