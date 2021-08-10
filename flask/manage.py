# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import Config

try:
    activate_this = '{0}/venv/bin/activate_this.py'.format(Config.ROOT_DIR)
    with open(activate_this) as f:
        exec(f.read(), dict(__file__=activate_this))
except FileNotFoundError:
    activate_this = '{0}/venv/Scripts/activate_this.py'.format(Config.ROOT_DIR)
    with open(activate_this) as f:
        exec(f.read(), dict(__file__=activate_this))

from apps.controllers.router import app as application
from apps.common.commands.manager import manager

if __name__ == '__main__':
    manager.run()
