import os
import sys
import select
import socket
from tests.tests import *
from client.client_log_config import *
from server.server_log_config import *
from server.server import *
from common.jim_log import *
from common.config import *

class Client:
    def __init__(self, host, port):
        self.address = (host, port)
        self.sock = socket.socket()
        self.sock.setblocking(True)
        self.sock.settimeout(1.0)

        while True:
            try:
                self.sock.connect(self.address)
                client_log.debug(f'Successfully connected to server')
                break
            except socket.error:
                client_log.info('Coldn\'t connect to server...')
                time.sleep(1)
            except KeyboardInterrupt:
                client_log.info('Ctrl+C detected. Exit.')
                print('\n', 'Ctrl+C detected. Exit.')
                self.sock.close()
                sys.exit()

    @decolog
    def send_request(self, request):
        byte_request = convert(request)
        self.sock.send(byte_request)
        client_log.debug(f'Successfully sent message: {byte_request}')

    @decolog
    def get_response(self, size=SIZE):
        try:
            print('1')
            byte_response = self.sock.recv(size)
            print('2')
            ##            client_log.debug(f'Successfully receive response: {byte_response}')
            ##            response = convert(byte_response)
            response = byte_response
        except OSError:
            response = ''
            self.sock.close()
            client_log.debug(f'Socket was closed.')

        return response

    @decolog
    def parse_response(self, response):
        '''
        Parse message
        '''
        client_log.info(f'Received message: {response}')

        if 'response' in response and response['response'] == 200:
            result = input('Enter your message: ')
        else:
            client_log.info(f'Something went wrong.')

        return result