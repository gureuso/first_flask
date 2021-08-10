# -*- coding: utf-8 -*-
import importlib
import os
import re


class BlueprintRegister(object):
    def __init__(self, app, module_path, controller_name):
        self.app = app
        self.module_path = module_path
        self.controller_name = controller_name
        self.controller_path = self.app.root_path
        self.directories = []

    def register(self):
        self.find_dir(self.controller_path)
        for dir_path in self.directories:
            dir_path = dir_path[1:].replace('/', '.')
            module_path = '{}.{}.{}'.format(self.module_path, dir_path, self.controller_name)
            module = importlib.import_module(module_path)
            self.app.register_blueprint(module.app)

    def find_dir(self, path):
        files = os.listdir(path)
        for file_name in files:
            isdir = os.path.isdir('{}/{}'.format(path, file_name))
            if not isdir:
                continue
            ignore = self.ignore(file_name)
            if ignore:
                continue
            self.append_dir(path, file_name)

    def append_dir(self, path, file_name):
        dir_path = '{}/{}'.format(path, file_name)
        self.directories.append(dir_path.replace(self.controller_path, ''))
        self.find_dir(dir_path)

    def ignore(self, name):
        # __pycache__/
        if re.match('__.*__', name):
            return True
        return False
