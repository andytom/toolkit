# -*- coding: utf-8 -*-
"""
    table_maker.tests
    ~~~~~~~~~~~~~~~~~
    Tests for table_maker.

    :copyright: (c) 2015 by Thomas O'Donnell.
    :license: BSD, see LICENSE for more details.
"""
import codecs
import os
from flask import Flask
from flask.ext.testing import TestCase

import table_maker


class BaseTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.register_blueprint(table_maker.table_maker)
        return app

    def _load_data_from_file(self, filename):
        cwd = os.path.dirname(__file__)
        resources = os.path.join(cwd, 'resources')
        input_file = os.path.join(resources, '{}.csv'.format(filename))
        output_file = os.path.join(resources, '{}.out'.format(filename))

        with codecs.open(input_file, 'r', 'utf8') as f:
            csv = f.read()

        with codecs.open(output_file, 'r', 'utf8') as f:
            expected = f.read()

        return csv, expected


#-----------------------------------------------------------------------------#
# Helper Functions Test Cases
#-----------------------------------------------------------------------------#
class ProcessStringTestCase(BaseTestCase):
    def _test_from_file(self, filename, **options):
        """
        Helper method to wrap the running of tests from a file.

        Takes an input filename and optional args for process_string.

        There must exist a filename.csv and a filename.out in the resources
        dir.
        """
        csv, expected = self._load_data_from_file(filename)
        res = table_maker.process_string(csv, **options)
        self.assertEqual(res, expected)

    def test_simple_file(self):
        self._test_from_file('simple')

    def test_complex_file(self):
        self._test_from_file('complex')

    def test_trailing_whitespace(self):
        self._test_from_file('trailing_whitespace')

    def test_alignment_left(self):
        self._test_from_file('alignment_l', table_align='l')

    def test_alignment_center(self):
        self._test_from_file('alignment_c', table_align='c')

    def test_alignment_right(self):
        self._test_from_file('alignment_r', table_align='r')

    def test_no_header(self):
        self._test_from_file('no_header', add_header=False)

    def test_alignment_center_no_headers(self):
        self._test_from_file('alignment_c_no_header', table_align='c',
                             add_header=False)

    def test_one_line_no_headers(self):
        self._test_from_file('one_line', add_header=False)


#-----------------------------------------------------------------------------#
# Blueprint Test Cases
#-----------------------------------------------------------------------------#
class AppTestCase(BaseTestCase):
    def test_page_load(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue("Table Maker" in rv.data)

    def test_valid_form_submit(self):
        csv, out = self._load_data_from_file('alignment_l')
        rv = self.client.post('/', data={'csv_string': csv,
                                         'table_align': 'l',
                                         'add_header': 'true'})
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(out in rv.data)

    def test_valid_form_submit_no_header(self):
        csv, out = self._load_data_from_file('no_header')
        rv = self.client.post('/', data={'csv_string': csv,
                                         'table_align': 'l',
                                         'add_header': 'false'})
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(out in rv.data)

    def test_valid_form_submit_alignment_and_header(self):
        csv, out = self._load_data_from_file('alignment_c')
        rv = self.client.post('/', data={'csv_string': csv,
                                         'table_align': 'c',
                                         'add_header': 'true'})
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(out in rv.data)

    def test_valid_form_submit_header(self):
        csv, out = self._load_data_from_file('alignment_c_no_header')
        rv = self.client.post('/', data={'csv_string': csv,
                                         'table_align': 'c',
                                         'add_header': 'false'})
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(out in rv.data)

    def test_valid_form_one_line_header(self):
        csv, out = self._load_data_from_file('one_line')
        rv = self.client.post('/', data={'csv_string': csv,
                                         'table_align': 'l',
                                         'add_header': 'false'})
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(out in rv.data)

    def test_empty_form_submit(self):
        rv = self.client.post('/')
        self.assertFalse('Output' in rv.data)
