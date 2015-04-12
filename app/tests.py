# -*- coding: utf-8 -*-
"""
    tests.py
    ~~~~~~~~
    Application tests for Toolkit.

    :copyright: (c) 2015 by Thomas O'Donnell.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.testing import TestCase

import app


class AppTestCase(TestCase):
    def create_app(self):
        return app.app

    def test_index_load(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
        # Check for links to the tools
        self.assertTrue('/base64_utils/' in rv.data)
        self.assertTrue('/mkd_preview/' in rv.data)
        self.assertTrue('/table_maker/' in rv.data)
        # Check the Title is correct
        self.assertTrue('<title>Toolkit</title>' in rv.data)

    def test_404(self):
        rv = self.client.get("/not/a/real/page")
        self.assertEqual(rv.status_code, 404)
        self.assertTrue('404 - Not Found' in rv.data)

    def test_mkd_preview_registered(self):
        # Check correct tools at the correct urls.
        # The individual tools have their own tests
        rv = self.client.get("/mkd_preview/")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('<title>Toolkit - Markdown Preview</title>' in rv.data)

    def test_table_maker_registered(self):
        # Check correct tools at the correct urls.
        # The individual tools have their own tests
        rv = self.client.get("/table_maker/")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('<title>Toolkit - Table Maker</title>' in rv.data)

    def test_base64_utils_registered(self):
        # Check correct tools at the correct urls.
        # The individual tools have their own tests
        rv = self.client.get("/base64_utils/")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('<title>Toolkit - Base64 Utilities</title>' in rv.data)
