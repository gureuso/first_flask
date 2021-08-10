# -*- coding: utf-8 -*-
from flask import Blueprint, send_from_directory

from apps.common.response import ok
from config import Config

app = Blueprint('index', __name__, url_prefix='/')


@app.route('/', methods=['GET'])
def index():
    return ok('Index')


@app.route('favicon.ico')
def favicon():
    return send_from_directory(Config.STATIC_DIR, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
