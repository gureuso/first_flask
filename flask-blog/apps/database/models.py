# -*- coding: utf-8 -*-
from datetime import datetime

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


class CommentMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(), default=datetime.now())


class TestCommentModel(CommentMixin, db.Model):
    __tablename__ = 'test_comments'

    user_id = db.Column(db.Integer(), db.ForeignKey('test_users.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('test_posts.id'))
    parent_id = db.Column(db.Integer(), db.ForeignKey('test_comments.id'), nullable=True)


class CommentModel(CommentMixin, db.Model):
    __tablename__ = 'comments'

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))
    parent_id = db.Column(db.Integer(), nullable=True)

    test_model = TestCommentModel


Comment = get_model(CommentModel)


class ViewMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.now())


class TestViewModel(ViewMixin, db.Model):
    __tablename__ = 'test_views'

    user_id = db.Column(db.Integer(), db.ForeignKey('test_users.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('test_posts.id'))


class ViewModel(ViewMixin, db.Model):
    __tablename__ = 'views'

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))

    test_model = TestViewModel


View = get_model(ViewModel)


class TagMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))


class TestTagModel(TagMixin, db.Model):
    __tablename__ = 'test_tags'

    post_id = db.Column(db.Integer(), db.ForeignKey('test_posts.id'))


class TagModel(TagMixin, db.Model):
    __tablename__ = 'tags'

    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))

    test_model = TestTagModel


Tag = get_model(TagModel)


class PostMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(), default=datetime.now())


class TestPostModel(PostMixin, db.Model):
    __tablename__ = 'test_posts'

    user_id = db.Column(db.Integer(), db.ForeignKey('test_users.id'))

    tags = db.relationship('TestTagModel', backref='post')


class PostModel(PostMixin, db.Model):
    __tablename__ = 'posts'

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    tags = db.relationship('TagModel', backref='post')

    test_model = TestPostModel


Post = get_model(PostModel)


class UserMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True)
    nickname = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(255))


class TestUserModel(UserMixin, flask_login.UserMixin, db.Model):
    __tablename__ = 'test_users'

    posts = db.relationship('TestPostModel', backref='user')
    comments = db.relationship('TestCommentModel', backref='user')


class UserModel(UserMixin, flask_login.UserMixin, db.Model):
    __tablename__ = 'users'

    posts = db.relationship('PostModel', backref='user')
    comments = db.relationship('CommentModel', backref='user')

    test_model = TestUserModel


User = get_model(UserModel)


@login_manager.user_loader
def member_loader(user_id):
    return User.query.filter(User.id == user_id).first()
