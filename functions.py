import json
import time
import logging

CODING = 'utf-8'

def act_time(time_):
    local_time = time.localtime(time_)
    t = time.strftime('%d.%m.%Y - %H:%M:%S', local_time)
    return t

def convert(data):
    result = None
    if isinstance(data, bytes):
        try:
            result = json.loads(data.decode(CODING))
        except TypeError:
            print('wrong data format!')
    elif isinstance(data, dict):
        try:
            result = json.dumps(data).encode(CODING)
        except TypeError:
            print('wrong data format!')
    else:
        print('wrong data format!')
    return result

def show_log(byte_request, count):
    pass

'''    request = convert(byte_request)
    account_name = request['user']['account_name']
    time_unix = request['time']
    time_ = act_time(time_unix)
    print('connection # {} // request from {} // sent time {}\n'.format(count, account_name, time_))
'''

def init_log():
    pass

def write_log(msg):
    pass
