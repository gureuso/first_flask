# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email


class SignInForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(message='필수 값입니다.'), Email(message='올바른 이메일 형식이 아닙니다.')])
    password = PasswordField('password', validators=[DataRequired(message='필수 값입니다.'),
                                                     Length(max=20, message='20자를 넘을 수 없습니다.')])


class SignUpForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(message='필수 값입니다.'), Email(message='올바른 이메일 형식이 아닙니다.')])
    password = PasswordField('password', validators=[DataRequired(message='필수 값입니다.'),
                                                     Length(max=20, message='20자를 넘을 수 없습니다.')])
    nickname = StringField('nickname', validators=[DataRequired(message='필수 값입니다.'),
                                                   Length(max=20, message='20자를 넘을 수 없습니다.')])
