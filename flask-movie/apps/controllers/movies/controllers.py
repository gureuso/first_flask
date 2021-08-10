# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

from apps.common.auth import signin_required
from apps.database.models import Movie

app = Blueprint('movies', __name__, url_prefix='/movies')


@app.route('', methods=['GET'])
@signin_required
def index():
    return ''
