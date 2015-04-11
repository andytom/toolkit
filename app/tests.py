from flask.ext.testing import TestCase
import app


class AppTestCase(TestCase):
    def create_app(self):
        return app.app

    def test_index_load(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('/base64_utils/' in rv.data)
        self.assertTrue('/mkd_preview/' in rv.data)
        self.assertTrue('/table_maker/' in rv.data)

    def test_404(self):
        rv = self.client.get("/not/a/real/page")
        self.assertEqual(rv.status_code, 404)

    def test_mkd_preview_registered(self):
        rv = self.client.get("/mkd_preview/")
        self.assertEqual(rv.status_code, 200)

    def test_table_maker_registered(self):
        rv = self.client.get("/table_maker/")
        self.assertEqual(rv.status_code, 200)

    def test_base64_utils_registered(self):
        rv = self.client.get("/base64_utils/")
        self.assertEqual(rv.status_code, 200)
