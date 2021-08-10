# -*- coding: utf-8 -*-
import unittest2

from apps.controllers.router import app
from apps.database.models import Test


class TestDatabase(unittest2.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_connect_db(self):
        rows = Test.query.filter_by(message='test01').all()
        self.assertEqual(len(rows), 0)


if __name__ == '__main__':
    unittest2.main()
