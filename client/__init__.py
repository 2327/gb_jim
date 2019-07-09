from common.config import *
from client.client_log_config import *
import os

try:
    os.mkdir(LOG_PATH)
except OSError:
    client_log.debug('Creation of the directory {LOG_PATH} failed')
else:
    client_log.debug('Successfully created the directory {LOG_PATH}')
