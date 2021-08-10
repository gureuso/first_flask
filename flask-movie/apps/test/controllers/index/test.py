# -*- coding: utf-8 -*-
import json
import unittest2

from apps.controllers.router import app


class Test(unittest2.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data.decode('utf-8'))
        self.assertEqual(data['data'], 'Index')


if __name__ == '__main__':
    unittest2.main()
