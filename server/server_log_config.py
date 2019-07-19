import logging
import time
import os

LOG_PATH = 'log'

loddate = time.strftime('%d-%m-%Y')
formatter = logging.Formatter('%(asctime)s %(levelname)-10s %(message)s')
server_log = logging.getLogger('server_log')

server_log_file = logging.FileHandler(f'log/server-{loddate}.log')
server_log_file.setFormatter(formatter)
server_log.setLevel(logging.INFO)
server_log.addHandler(server_log_file)

server_log_stdout = logging.StreamHandler()
server_log_stdout.setFormatter(formatter)
server_log.addHandler(server_log_stdout)

try:
    os.mkdir(LOG_PATH)
except OSError:
    server_log.debug('Creation of the directory {LOG_PATH} failed')
else:
    server_log.debug('Successfully created the directory {LOG_PATH}')

