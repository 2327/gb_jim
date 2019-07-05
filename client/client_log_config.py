import logging

logging.basicConfig(filename="log/client.log", format="%(asctime)s %(levelname)-10s %(message)s", level=logging.DEBUG)
client_log = logging.getLogger('client')
