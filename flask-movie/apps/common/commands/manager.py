# -*- coding: utf-8 -*-
import unittest2
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


from apps.controllers.router import app
from apps.database.session import db
from config import Config, JsonConfig

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """test code"""
    JsonConfig.set_data('TESTING', True)

    loader = unittest2.TestLoader()
    start_dir = '{0}/apps'.format(Config.ROOT_DIR)
    suite = loader.discover(start_dir)

    runner = unittest2.TextTestRunner()
    r = runner.run(suite)

    JsonConfig.set_data('TESTING', False)

    if r.wasSuccessful():
        print('success')
    else:
        print('fail')
        exit(1)


@manager.option('-h', '--host', dest='host', default=Config.APP_HOST)
@manager.option('-p', '--port', dest='port', default=Config.APP_PORT)
def runserver(host, port):
    """run flask server"""
    app.run(host=host, port=int(port))
