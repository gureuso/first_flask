# -*- coding: utf-8 -*-
import unittest2
from flask import url_for

from apps.common.auth import SHA256
from apps.controllers.router import app
from apps.database.models import User, Post, Tag
from apps.database.session import db
from config import JsonConfig


class Test(unittest2.TestCase):
    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    @classmethod
    def setUpClass(cls):
        JsonConfig.set_data('TESTING', True)
        cls.u1 = User(email='wyun13043@gmail.com', nickname='gureuso01', password=SHA256.encrypt('1234'))
        cls.u2 = User(email='wyun13043@daum.net', nickname='gureuso02', password=SHA256.encrypt('1234'))
        db.session.add(cls.u1)
        db.session.add(cls.u2)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        Tag.query.delete()
        Post.query.delete()
        User.query.delete()
        db.session.commit()
        JsonConfig.set_data('TESTING', False)

    def test_create_post(self):
        with self.app:
            self.app.post(url_for('users.signin'), data=dict(email='wyun13043@gmail.com', password='1234'))
            result = self.app.post('/apis/posts', data=dict(title='test 01', content='test 01', tags='test,cat'))
            self.assertEqual(result.status_code, 200)

            result = self.app.post('/apis/posts', data=dict(title='test 02', content='test 02', tags='test,dog'))
            self.assertEqual(result.status_code, 200)

    def test_get_post(self):
        with self.app:
            self.app.post(url_for('users.signin'), data=dict(email='wyun13043@gmail.com', password='1234'))
            result = self.app.get('/apis/posts?q=test')
            self.assertEquals(len(result.json['data']), 2)

            result = self.app.get('/apis/posts')
            self.assertEquals(len(result.json['data']), 2)

            result = self.app.get('/apis/posts?q=cat')
            self.assertEquals(len(result.json['data']), 1)

    def test_update_post(self):
        with self.app:
            self.app.post(url_for('users.signin'), data=dict(email='wyun13043@gmail.com', password='1234'))
            result = self.app.put('/apis/posts/9999', data=dict(title='test 03', content='test 03', tags='test,dog'))
            self.assertEquals(result.status_code, 404)

            post = Post.query.first()
            result = self.app.put('/apis/posts/{}'.format(post.id), data=dict(title='test 03', content='test 03', tags='test,dog'))
            self.assertEquals(result.status_code, 200)

            self.app.get(url_for('users.signout'))
            self.app.post(url_for('users.signin'), data=dict(email='wyun13043@daum.net', password='1234'))
            result = self.app.put('/apis/posts/{}'.format(post.id), data=dict(title='test 04', content='test 04', tags='test,dog'))
            self.assertEquals(result.status_code, 403)


if __name__ == '__main__':
    unittest2.main()
