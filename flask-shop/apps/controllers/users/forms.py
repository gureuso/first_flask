# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email


class ProfileForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(message='필수 값입니다.'),
                                                   Length(max=30, message='30자를 넘을 수 없습니다.')])
    address = StringField('address', validators=[DataRequired(message='필수 값입니다.'),
                                                 Length(max=255, message='255자를 넘을 수 없습니다.')])
    phone = StringField('phone', validators=[DataRequired(message='필수 값입니다.'),
                                             Length(max=20, message='20자를 넘을 수 없습니다.')])
    detail_address = StringField('detail_address', validators=[DataRequired(message='필수 값입니다.'),
                                                               Length(max=255, message='255자를 넘을 수 없습니다.')])


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
