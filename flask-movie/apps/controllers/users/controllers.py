# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user

from apps.common.auth import SHA256, already_signin
from apps.controllers.users.forms import SignInForm, SignUpForm
from apps.database.models import User
from apps.database.session import db

app = Blueprint('users', __name__, url_prefix='/users')


@app.route('/signup', methods=['GET', 'POST'])
@already_signin
def signup():
    return ''


@app.route('/signin', methods=['GET', 'POST'])
@already_signin
def signin():
    return ''


@app.route('signout', methods=['GET'])
def signout():
    return ''
