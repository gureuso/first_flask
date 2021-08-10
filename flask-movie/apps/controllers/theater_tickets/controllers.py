# -*- coding: utf-8 -*-
from flask import Blueprint, request

from apps.common.auth import signin_required
from apps.common.response import ok, error
from apps.database.models import TheaterTicket, Showtime
from apps.database.session import db

app = Blueprint('theater_tickets', __name__, url_prefix='/theater_tickets')


@app.route('', methods=['POST'])
@signin_required
def create():
    return ok()
