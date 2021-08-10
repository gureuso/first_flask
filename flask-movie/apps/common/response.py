# -*- coding: utf-8 -*-
import flask
import json

from config import Config


def make_response(data, code):
    status_code = int(code / 100)
    resp = flask.make_response(data, status_code)
    resp.headers['Content-Type'] = 'application/json'
    return resp


def ok(data=None, code=20000):
    res = json.dumps({
        'code': code,
        'data': data or {}
    })
    return make_response(res, code)


def error(code, message=None):
    if not message:
        message = Config.ERROR_CODE[code]

    res = json.dumps({
        'code': code,
        'message': message
    })
    return make_response(res, code)
