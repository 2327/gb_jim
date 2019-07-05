'''
На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.
'''

import logging

logging.basicConfig(filename="log/server.log", format="%(asctime)s %(levelname)-10s %(message)s", level=logging.INFO)
server_log = logging.getLogger('server')
