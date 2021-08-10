# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user

from apps.common.auth import SHA256, already_signin, signin_required
from apps.controllers.carts import get_carts
from apps.controllers.users.forms import SignInForm, SignUpForm, ProfileForm
from apps.database.models import User, Category, Order, Delivery
from apps.database.session import db

app = Blueprint('users', __name__, url_prefix='/users')


@app.route('/profile', methods=['GET', 'POST'])
@signin_required
def profile():
    form = ProfileForm()

    delivery = Delivery.query.filter(Delivery.user_id == current_user.id).first()
    if form.validate_on_submit():
        if delivery:
            delivery.username = form.username.data
            delivery.phone = form.phone.data
            delivery.address = form.address.data
            delivery.detail_address = form.detail_address.data
        else:
            delivery = Delivery(username=form.username.data, address=form.address.data,
                                detail_address=form.detail_address.data, phone=form.phone.data,
                                user_id=current_user.id)
            db.session.add(delivery)
        db.session.commit()
        return redirect(url_for('index.index'))

    if delivery:
        form.username.data = delivery.username
        form.phone.data = delivery.phone
        form.address.data = delivery.address
        form.detail_address.data = delivery.detail_address

    categories = Category.query.all()
    orders = Order.query.filter(Order.user_id == current_user.id).all()
    return render_template('users/profile.html', categories=categories, orders=orders, carts=get_carts(), form=form)


@app.route('/signin', methods=['GET', 'POST'])
@already_signin
def signin():
    form = SignInForm()

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if not user:
            form.email.errors.append('가입하지 않은 이메일 입니다.')
            return render_template('users/signin.html', form=form)
        if user.password != SHA256.encrypt(form.password.data):
            form.password.errors.append('비밀번호가 일치하지 않습니다.')
            return render_template('users/signin.html', form=form)

        login_user(user)
        return redirect(url_for('index.index'))
    return render_template('users/signin.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
@already_signin
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        email_user = User.query.filter(User.email == form.email.data).first()
        nickname_user = User.query.filter(User.nickname == form.nickname.data).first()
        if email_user:
            if email_user.email == form.email.data:
                form.email.errors.append('이미 가입된 이메일입니다.')
        if nickname_user:
            if nickname_user.nickname == form.nickname.data:
                form.nickname.errors.append('이미 가입된 닉네임입니다.')

        if form.email.errors or form.nickname.errors:
            return render_template('users/signup.html', form=form)

        user = User(email=form.email.data, nickname=form.nickname.data, password=SHA256.encrypt(form.password.data), point=1000000)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('index.index'))
    return render_template('users/signup.html', form=form)


@app.route('signout', methods=['GET'])
def signout():
    logout_user()
    return redirect(url_for('users.signin'))
