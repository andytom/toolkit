import base64
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

    def _base64_encode(self, name):
        full_name = self._gen_full_path(name)
        with open(full_name, 'rb') as f:
            raw = f.read()
        return base64.b64encode(raw)


#-----------------------------------------------------------------------------#
# Helper Functions Test Cases
#-----------------------------------------------------------------------------#
class ProcessBase64TestCase(BaseTestCase):
    def _guess_extention(self, name):
        full_name = self._gen_full_path(name)
        with open(full_name, 'rb') as f:
            res = base64_utils.guess_extention(f.read())
        return res

    def test_creates_unique_filenames(self):
        f = base64_utils.create_filename('.txt')
        g = base64_utils.create_filename('.txt')
        self.assertFalse(f == g)

    def test_guess_extention_txt(self):
        res = self._guess_extention('test.txt')
        self.assertEqual(res, '.txt')

    def test_guess_extention_doc(self):
        res = self._guess_extention('test.doc')
        self.assertEqual(res, '.doc')

    def test_guess_extention_pdf(self):
        res = self._guess_extention('test.pdf')
        self.assertEqual(res, '.pdf')

    def test_base64_to_stringio(self):
        b64_str = self._base64_encode('test.txt')
        res, _ = base64_utils.base64_to_stringio(b64_str)
        with open(self._gen_full_path('test.txt')) as f:
            self.assertEqual(f.read(), res.read())

    def test_base64_to_stringio_with_filename(self):
        b64_str = self._base64_encode('test.txt')
        res, filename = base64_utils.base64_to_stringio(b64_str, 'test.txt')
        self.assertEqual('test.txt', filename)
        with open(self._gen_full_path('test.txt')) as f:
            self.assertEqual(f.read(), res.read())


#-----------------------------------------------------------------------------#
# Blueprint Test Cases
#-----------------------------------------------------------------------------#
class AppTestCase(BaseTestCase):
    def _post_file(self, filename, send_filename, content_type):
        b64_str = self._base64_encode(filename)

        data = {'content': b64_str}
        if send_filename:
            data['filename'] = filename

        rv = self.client.post("/", data=data)
        self.assertEqual(rv.status_code, 200)

        # Check the content matched that of the input file
        with open(self._gen_full_path(filename), 'rb') as f:
            self.assertEqual(rv.data, f.read())

        # Check the content_type is correct
        self.assertEqual(rv.content_type, content_type)

        # Check the correct filename is in the Content-Disposition
        if send_filename:
            self.assertEqual('attachment; filename={}'.format(filename),
                rv.headers['Content-Disposition'])

    def test_page_load(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)

    def test_send_txt(self):
        self._post_file('test.txt', False, 'text/plain; charset=utf-8')
        self._post_file('test.txt', True, 'text/plain; charset=utf-8')

    def test_send_pdf(self):
        self._post_file('test.pdf', True, 'application/pdf')
        self._post_file('test.pdf', False, 'application/pdf')

    def test_send_doc(self):
        self._post_file('test.doc', True, 'application/msword')
        self._post_file('test.doc', False, 'application/msword')
