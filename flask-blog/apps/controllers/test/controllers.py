# -*- coding: utf-8 -*-
import requests
from flask import Blueprint, abort, render_template, request

from apps.common.response import ok, error
from apps.database.models import Test
from apps.database.session import db
from .forms import TestForm

app = Blueprint('test', __name__, url_prefix='/test')


@app.route('', methods=['GET'])
def get_tests():
    tests = Test.query.all()
    return render_template('test/test.html', tests=tests)


@app.route('', methods=['POST'])
def create_test():
    test = Test(message='Hello World!!!')
    db.session.add(test)
    db.session.commit()
    return ok()


@app.route('/<int:test_id>', methods=['DELETE'])
def delete_test(test_id):
    test = Test.query.filter(Test.id == test_id).first()
    db.session.delete(test)
    db.session.commit()
    return ok()


@app.route('/<int:test_id>', methods=['PUT'])
def update_test(test_id):
    test = Test.query.filter(Test.id == test_id).first()
    test.message = 'Hello World2!!!'
    db.session.commit()
    return ok()


@app.route('/ping', methods=['GET'])
def ping():
    return ok('pong')


@app.route('/proxy', methods=['GET', 'POST'])
def proxy():
    args = request.args
    form = request.form
    url = args.get('url')

    if not url:
        return error(50000)

    if request.method == 'GET':
        res = requests.get(url=url)
    else:
        res = requests.post(url=url, data=form)

    return ok(dict(url=res.url, data=res.text, code=res.status_code))


@app.route('/403', methods=['GET'])
def forbidden():
    return abort(403)


@app.route('/404', methods=['GET'])
def page_not_found():
    return abort(404)


@app.route('/410', methods=['GET'])
def gone():
    return abort(410)


@app.route('/500', methods=['GET'])
def internal_server_error():
    return abort(500)


@app.route('/html', methods=['GET', 'POST'])
def html():
    form = TestForm()

    fruits = {'apple': '사과', 'orange': '오렌지', 'grape': '포도'}
    for key in fruits.keys():
        form.fruits.choices.append((key, fruits[key]))

    if form.validate_on_submit():
        return render_template('test/html.html', form=form, result='저장했습니다.')

    return render_template('test/html.html', form=form)
