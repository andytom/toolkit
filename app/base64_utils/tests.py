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


class AppTestCase(BaseTestCase):
    def test_page_load(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
