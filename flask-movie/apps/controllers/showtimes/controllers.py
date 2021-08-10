# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from datetime import datetime, timedelta

from sqlalchemy import and_

from apps.common.auth import signin_required
from apps.database.models import Showtime, Movie, TheaterTicket, Theater

app = Blueprint('showtimes', __name__, url_prefix='/showtimes')


@app.route('', methods=['GET'])
@signin_required
def index():
    return ''
