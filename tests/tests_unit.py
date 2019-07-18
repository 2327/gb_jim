import unittest
from common.converters import *
from common.formatters import *


class TestTime(unittest.TestCase):

    def test_actual_time(self):
        self.assertEqual(act_time(int('1561845014')),('30.06.2019 - 00:50:14'))

    def test_convert_dict(self):
        self.assertIsNone(convert(['{"action": "presence", "2": "2"}']))

    def test_convert_empty(self):
        self.assertIsNone(convert(' '))


if __name__ == "__main__":
    unittest.main()