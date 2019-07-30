import os
import sys
import select
import socket
import threading
from tests.tests import *
from client.client_log_config import *
from server.server_log_config import *
from server.server import *
from common.jim_log import *
from common.config import *

import random


class Client:
    def __init__(self, host, port, client_name):
        self.address = (host, port)
        self.client_name = client_name

    @decolog
    def get_connect(self):
        self.sock = socket.socket()
        self.sock.setblocking(True)
        self.sock.settimeout(0.2)

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
        if request == 'presence':
            request = {"action": "presence", "time": time.time(), "client": self.client_name}
        elif request == 'get_contacts':
            print('1')
            request = {"action": "get_contacts", "time": time.time(), "client": self.client_name}
        byte_request = convert(request)
        print('2', byte_request)
        self.sock.send(byte_request)
        client_log.debug(f'Successfully sent message: {byte_request}')

    @decolog
    def get_response(self, size=SIZE):
        try:
            client_log.debug('Trying receive response...')
            byte_response = self.sock.recv(size)
            client_log.debug(f'Successfully receive response: {byte_response}')
            response = convert(byte_response)
            if response != 'empty':
                for message in response['messages']:
                    print(f'You get message: {OKGREEN}{message}{ENDC}')
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