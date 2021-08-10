# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length


class TestForm(FlaskForm):
    fruits = SelectField('fruits', validators=[DataRequired()], choices=[])
    username = StringField('username', validators=[DataRequired(), Length(max=10, message='10자를 넘을 수 없습니다.')])
    amount = IntegerField('amount', validators=[DataRequired(),
                                                NumberRange(min=1, max=10000, message='자릿수를 초과했습니다.')])
