import codecs
import os
import unittest
import table_maker


class ProcessStringTestCase(unittest.TestCase):
    def _test_from_file(self, filename, **options):
        """
        Helper method to wrap the running of tests from a file.

        Takes an input filename and optional args for process_string.

        There must exist a filename.csv and a filename.out in the resources
        dir.
        """
        cwd = os.path.dirname(__file__)
        resources = os.path.join(cwd, 'resources')
        input_file = os.path.join(resources, '{}.csv'.format(filename))
        output_file = os.path.join(resources, '{}.out'.format(filename))

        with codecs.open(input_file, 'r', 'utf8') as f:
            csv = f.read()
            res = table_maker.process_string(csv, **options)

        with codecs.open(output_file, 'r', 'utf8') as f:
            expected = f.read()

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
