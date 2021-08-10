# -*- coding: utf-8 -*-
from flask import Flask

from apps.common.register import BlueprintRegister
from apps.common.response import error

from config import Config

app = Flask(__name__, template_folder=Config.TEMPLATES_DIR, static_folder=Config.STATIC_DIR)
app.config.from_object(Config.from_app_mode())
BlueprintRegister(app=app, module_path='apps.controllers', controller_name='controllers').register()


@app.errorhandler(403)
def forbidden(err):
    return error(40300)


@app.errorhandler(404)
def page_not_found(err):
    return error(40400)


@app.errorhandler(410)
def gone(err):
    return error(41000)


@app.errorhandler(500)
def internal_server_error(err):
    return error(50000)
