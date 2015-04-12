# -*- coding: utf-8 -*-
"""
    mkd_preview.tests
    ~~~~~~~~~~~~~~~~~
    Tests for mkd_preview.

    :copyright: (c) 2015 by Thomas O'Donnell.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask
from flask.ext.testing import TestCase

import mkd_preview


class AppTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.register_blueprint(mkd_preview.mkd_preview)
        return app

    def test_page_load(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue("Markdown Live Preview" in rv.data)
