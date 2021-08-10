# -*- coding: utf-8 -*-
from redis import Redis
from flask_sqlalchemy import SQLAlchemy

from config import Config
from apps.controllers.router import app

db = SQLAlchemy(app)
cache = Redis(host=Config.REDIS_HOST, password=Config.REDIS_PASSWD)


@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()
