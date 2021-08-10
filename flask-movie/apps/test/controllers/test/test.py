# -*- coding: utf-8 -*-
import json
import unittest2

from apps.controllers.router import app


class Test(unittest2.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_ping(self):
        result = self.app.get('/test/ping')
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data.decode('utf-8'))
        self.assertEqual(data['data'], 'pong')

    def test_get_403(self):
        result = self.app.get('/test/403')
        self.assertEqual(result.status_code, 403)
        data = json.loads(result.data.decode('utf-8'))
        self.assertEqual(data['code'], 40300)

    def test_get_404(self):
        result = self.app.get('/test/404')
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data.decode('utf-8'))
        self.assertEqual(data['code'], 40400)

    def test_get_410(self):
        result = self.app.get('/test/410')
        self.assertEqual(result.status_code, 410)
        data = json.loads(result.data.decode('utf-8'))
        self.assertEqual(data['code'], 41000)

    def test_get_500(self):
        result = self.app.get('/test/500')
        self.assertEqual(result.status_code, 500)
        data = json.loads(result.data.decode('utf-8'))
        self.assertEqual(data['code'], 50000)

    def test_get_html(self):
        result = self.app.get('/test/html')
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    unittest2.main()
