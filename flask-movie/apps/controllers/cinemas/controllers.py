# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request

from apps.common.auth import signin_required
from apps.database.models import Cinema

app = Blueprint('cinemas', __name__, url_prefix='/cinemas')


@app.route('', methods=['GET'])
@signin_required
def index():
    return ''
