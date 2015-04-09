import os
from flask import Flask
from flask.ext.testing import TestCase

import base64_utils


class BaseTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.register_blueprint(base64_utils.base64_utils)
        return app

    def _gen_full_path(self, filename):
        cwd = os.path.dirname(__file__)
        resources = os.path.join(cwd, 'resources')
        return os.path.join(resources, filename)


class ProcessBase64TestCase(BaseTestCase):
    def test_creates_unique_filenames(self):
        f = base64_utils.create_filename('.txt')
        g = base64_utils.create_filename('.txt')
        self.assertFalse(f == g)

    def test_guess_extention_txt(self):
        filename = self._gen_full_path('test.txt')
        with open(filename, 'rb') as f:
            res = base64_utils.guess_extention(f.read())
        self.assertEqual(res, '.txt')


class AppTestCase(BaseTestCase):
    def test_page_load(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
