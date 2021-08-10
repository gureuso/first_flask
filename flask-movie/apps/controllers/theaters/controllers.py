# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user

from apps.common.auth import signin_required
from apps.database.models import Showtime, Theater, TheaterTicket

app = Blueprint('theaters', __name__, url_prefix='/theaters')


@app.route('/<int:theater_id>/showtimes/<int:showtime_id>', methods=['GET'])
@signin_required
def detail(theater_id, showtime_id):
    return ''
