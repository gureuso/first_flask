# -*- coding: utf-8 -*-
import os
import json


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class JsonConfig:
    DATA = json.loads(open('{}/config.json'.format(ROOT_DIR)).read())

    @staticmethod
    def get_data(varname, value=None):
        return JsonConfig.DATA.get(varname) or os.environ.get(varname) or value

    @staticmethod
    def set_data(key, value):
        JsonConfig.DATA[key] = value
        with open('{}/config.json'.format(ROOT_DIR), 'w') as f:
            json.dump(JsonConfig.DATA, f, indent=4)


# app config
class Config:
    ROOT_DIR = ROOT_DIR
    STATIC_DIR = '{0}/static'.format(ROOT_DIR)
    TEMPLATES_DIR = '{0}/templates'.format(ROOT_DIR)
    ERROR_CODE = {
        40000: 'Bad Request',
        41000: 'Gone',
        40300: 'Forbidden',
        40400: 'Not Found',
        50000: 'Internal Server Error',
    }

    APP_MODE_PRODUCTION = 'production'
    APP_MODE_DEVELOPMENT = 'development'
    APP_MODE_TESTING = 'testing'

    APP_MODE = JsonConfig.get_data('APP_MODE', APP_MODE_PRODUCTION)
    APP_HOST = JsonConfig.get_data('APP_HOST', '0.0.0.0')
    APP_PORT = int(JsonConfig.get_data('APP_PORT', 80))

    DB_USER_NAME = JsonConfig.get_data('DB_USER_NAME', 'root')
    DB_USER_PASSWD = JsonConfig.get_data('DB_USER_PASSWD', 'password')
    DB_HOST = JsonConfig.get_data('DB_HOST', 'localhost')
    DB_NAME = JsonConfig.get_data('DB_NAME', 'flask')

    REDIS_HOST = JsonConfig.get_data('REDIS_HOST', 'localhost')
    REDIS_PASSWD = JsonConfig.get_data('REDIS_PASSWD')

    @staticmethod
    def from_app_mode():
        mode = {
            Config.APP_MODE_PRODUCTION: 'config.ProductionConfig',
            Config.APP_MODE_DEVELOPMENT: 'config.DevelopmentConfig',
            Config.APP_MODE_TESTING: 'config.TestingConfig',
        }
        return mode.get(Config.APP_MODE, mode[Config.APP_MODE_DEVELOPMENT])

    @staticmethod
    def database_url(dialect='mysql'):
        if dialect == 'mongodb':
            return '{}://{}:{}@{}'.format(dialect, Config.DB_USER_NAME, Config.DB_USER_PASSWD, Config.DB_HOST)

        return '{}://{}:{}@{}/{}?charset=utf8'.format(dialect, Config.DB_USER_NAME, Config.DB_USER_PASSWD,
                                                      Config.DB_HOST, Config.DB_NAME)


# flask config
class FlaskConfig:
    SECRET_KEY = '9022b99ae34ae74ec06bbeac8653b6c98a6ff9ee66ac4f96'
    SQLALCHEMY_DATABASE_URI = Config.database_url()
    # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class ProductionConfig(FlaskConfig):
    pass


class DevelopmentConfig(FlaskConfig):
    SQLALCHEMY_ECHO = True
    DEBUG = True
    TESTING = True


class TestingConfig(FlaskConfig):
    TESTING = True
