# -*- coding: utf-8 -*-
from flask import Blueprint

from apps.common.response import ok

app = Blueprint('rx', __name__, url_prefix='/rx')


@app.route('', methods=['GET'])
def index():
    return ok()
