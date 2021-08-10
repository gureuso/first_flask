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


class CategoryMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)


class TestCategoryModel(CategoryMixin, db.Model):
    __tablename__ = 'test_categories'

    products = db.relationship('TestProductModel', backref='category')


class CategoryModel(CategoryMixin, db.Model):
    __tablename__ = 'categories'

    products = db.relationship('ProductModel', backref='category')

    test_model = TestCategoryModel


Category = get_model(CategoryModel)


class ProductMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Integer)
    image_url = db.Column(db.String(255))


class TestProductModel(ProductMixin, db.Model):
    __tablename__ = 'test_products'

    category_id = db.Column(db.Integer(), db.ForeignKey('test_categories.id'))

    carts = db.relationship('TestCartModel', backref='product')
    orders = db.relationship('TestOrderModel', backref='product')


class ProductModel(ProductMixin, db.Model):
    __tablename__ = 'products'

    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))

    carts = db.relationship('CartModel', backref='product')
    orders = db.relationship('OrderModel', backref='product')

    test_model = TestProductModel


Product = get_model(ProductModel)


class CartMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class TestCartModel(CartMixin, db.Model):
    __tablename__ = 'test_carts'

    product_id = db.Column(db.Integer(), db.ForeignKey('test_products.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('test_users.id'))


class CartModel(CartMixin, db.Model):
    __tablename__ = 'carts'

    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    test_model = TestCartModel


Cart = get_model(CartModel)


class OrderMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now())


class TestOrderModel(OrderMixin, db.Model):
    __tablename__ = 'test_orders'

    product_id = db.Column(db.Integer(), db.ForeignKey('test_products.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('test_users.id'))
    delivery_id = db.Column(db.Integer(), db.ForeignKey('test_deliveries.id'))


class OrderModel(OrderMixin, db.Model):
    __tablename__ = 'orders'

    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    delivery_id = db.Column(db.Integer(), db.ForeignKey('deliveries.id'))

    test_model = TestCartModel


Order = get_model(OrderModel)


class DeliveryMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    address = db.Column(db.String(255))
    detail_address = db.Column(db.String(255))
    phone = db.Column(db.String(20))


class TestDeliveryModel(DeliveryMixin, db.Model):
    __tablename__ = 'test_deliveries'

    user_id = db.Column(db.Integer(), db.ForeignKey('test_users.id'))

    orders = db.relationship('TestOrderModel', backref='delivery')


class DeliveryModel(DeliveryMixin, db.Model):
    __tablename__ = 'deliveries'

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    orders = db.relationship('OrderModel', backref='delivery')

    test_model = TestCartModel


Delivery = get_model(DeliveryModel)


class UserMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True)
    nickname = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(255))
    point = db.Column(db.Integer)


class TestUserModel(UserMixin, flask_login.UserMixin, db.Model):
    __tablename__ = 'test_users'


class UserModel(UserMixin, flask_login.UserMixin, db.Model):
    __tablename__ = 'users'

    test_model = TestUserModel


User = get_model(UserModel)


@login_manager.user_loader
def member_loader(user_id):
    return User.query.filter(User.id == user_id).first()
