import unittest
import table_maker


class TestCase(unittest.TestCase):
    def test_process_string(self):
        test_string = u"1,2,3"
        output = table_maker.process_string(test_string)
        self.assertEqual(output, u"""+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
+---+---+---+""")

