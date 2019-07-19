import logging
import os

LOG_PATH = 'log'

formatter = logging.Formatter('%(asctime)s %(levelname)-10s %(message)s')
client_log = logging.getLogger('client_log')

client_log_file = logging.FileHandler('log/client.log')
client_log_file.setFormatter(formatter)
client_log.setLevel(logging.INFO)
client_log.addHandler(client_log_file)

client_log_stdout = logging.StreamHandler()
client_log_stdout.setFormatter(formatter)
client_log.addHandler(client_log_stdout)



