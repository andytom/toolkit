import codecs
import os
import unittest
import table_maker


class ProcessStringTestCase(unittest.TestCase):
    def _test_from_file(self,filename):
        cwd = os.path.dirname(__file__)
        resources = os.path.join(cwd, 'resources')
        input_file = os.path.join(resources, '{}.csv'.format(filename))
        output_file = os.path.join(resources, '{}.out'.format(filename))

        with codecs.open(input_file, 'r', 'utf8') as f:
            csv = f.read()
            res = table_maker.process_string(csv)

        with codecs.open(output_file, 'r', 'utf8') as f:
            expected = f.read()

        self.assertEqual(res, expected)

    def test_simple_file(self):
        self._test_from_file('simple')

    def test_complex_file(self):
        self._test_from_file('complex')
