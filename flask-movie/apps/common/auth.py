# -*- coding: utf-8 -*-
import hashlib
from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


class SHA256:
    @staticmethod
    def encrypt(value):
        return hashlib.sha256(value.encode()).hexdigest()

    @staticmethod
    def compare_with(a, b):
        return SHA256.encrypt(a) == SHA256.encrypt(b)


def already_signin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('showtimes.index'))
        return func(*args, **kwargs)
    return wrapper


def signin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('users.signin'))
        return func(*args, **kwargs)
    return wrapper
