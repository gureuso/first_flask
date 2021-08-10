# -*- coding: utf-8 -*-
import json
import unittest2

from apps.controllers.router import app


class Test(unittest2.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest2.main()
