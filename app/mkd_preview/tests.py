from flask import Flask
from flask.ext.testing import TestCase

import mkd_preview


class BaseTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.register_blueprint(mkd_preview.mkd_preview)
        return app


class AppTestCase(BaseTestCase):
    def test_page_load(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue("Markdown Live Preview" in rv.data)
