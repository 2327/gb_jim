'''
На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.
'''

import logging
import time

logname = str('log/server-' + time.strftime('%d-%m-%Y') + '.log')

logging.basicConfig(filename = logname, format = "%(asctime)s %(levelname)-10s %(message)s", level = logging.INFO)
server_log = logging.getLogger('server')
