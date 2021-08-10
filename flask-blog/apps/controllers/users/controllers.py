# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user

from apps.common.auth import SHA256, already_signin
from apps.controllers.users.forms import SignInForm, SignUpForm
from apps.database.models import User
from apps.database.session import db

app = Blueprint('users', __name__, url_prefix='/users')


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

        user = User(email=form.email.data, nickname=form.nickname.data, password=SHA256.encrypt(form.password.data))
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('index.index'))
    return render_template('users/signup.html', form=form)


@app.route('signout', methods=['GET'])
def signout():
    logout_user()
    return redirect(url_for('users.signin'))
