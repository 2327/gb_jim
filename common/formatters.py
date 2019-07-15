import time
from common.config import *

def act_time(time_):
    local_time = time.localtime(time_)
    t = time.strftime('%d.%m.%Y - %H:%M:%S', local_time)
    return t
