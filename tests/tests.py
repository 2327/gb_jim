from common.converters import *
from common.formatters import *

def test_actual_time():
    assert act_time(int('1561845014')) == '30.06.2019 - 00:50:14', 'test 1: Wrong operation time'

def test_convert_dict():
    assert convert('{"action": "presence", "2": "2"}') == None, 'test 2: Wrong operation empty data'

def test_convert_empty():
    assert convert(' ') == None, 'test 3: Wrong operation empty data'
