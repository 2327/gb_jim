import json
import logging
from common.config import *


def convert(data):
    logger = logging.getLogger(__name__)
    if isinstance(data, bytes):
        try:
            result = data.decode(CODING)
            if result == '':
                result = dict({"action": "empty", "ip": "ip"})
            else:
                result = json.loads(result)
        except TypeError:
            logger.info('wrong data format!')
    elif isinstance(data, dict):
        try:
            result = json.dumps(data).encode(CODING)
        except TypeError:
            logger.info('wrong data format!')
    elif isinstance(data, list):
        data = dict({"messages": data})
        try:
            result = json.dumps(data).encode(CODING)
        except TypeError:
            logger.info('wrong data format!')
    else:
        logger.info('wrong data format!')
        result = json.dumps(dict({"action": "error", "message": "wrong format"})).encode(CODING)
    return result

'''    request = convert(byte_request)
    account_name = request['user']['account_name']
    time_unix = request['time']
    time_ = act_time(time_unix)
    print('connection # {} // request from {} // sent time {}\n'.format(count, account_name, time_))
'''

def init_log():
    pass

def show_log(byte_request, count):
    pass

def write_log(msg):
    pass
