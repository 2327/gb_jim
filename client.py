#!/usr/bin/env python3

import sys
import socket
from tests.tests import *
from client.client_log_config import *


HOST = '127.0.0.1'
PORT = 7777
SIZE = 1024
CODING = 'utf-8'
CODES = {100: 'Base', 101: 'Important',
         200: 'OK', 201: 'Created',
         400: 'Wrong request', 401: 'Not authorized', 402: 'Wrong login/password',
         500: 'Server error'}
LOG_PATH = 'log'

class Client:
    def __init__(self, host, port):
        self.address = (host, port)
        self.sock = socket.socket()

        while True:
            try:
                client_log.debug(f'Successfully connected to server')
                self.sock.connect(self.address)
                break
            except socket.error:
                client_log.info('Coldn\'t connect to server...')
                time.sleep(1)
            except KeyboardInterrupt:
                client_log.info('Ctrl+C detected. Exit.')
                print('\n', 'Ctrl+C detected. Exit.')
                self.sock.close()
                sys.exit()

    def send_request(self, request):
        byte_request = convert(request)
        self.sock.send(byte_request)
        client_log.debug(f'Successfully send message: {byte_request}')

    def get_response(self, size=SIZE):
        byte_response = self.sock.recv(size)
        client_log.debug(f'Successfully receive message: {byte_response}')
        response = convert(byte_response)
        '''
        self.sock.close()
        client_log.debug(f'Socket was closed.')
        '''
        return response

    def parse_response(self, response):
        client_log.info(f'Received response: {response}')

        if 'response' in response and response['response'] == 200:
            result = input('Enter your message: ')
        else:
            client_log.info(f'Something went wrong.')

        return result

def cmd_client(params):
    '''
    TODO: need to add log options for foreground and verbose
          nedd add ConfigParser for working with config file
    '''

    host_ = HOST
    port_ = PORT

    if len(params) == 2:
        try:
            host, port = params[1].split('[')
            port = int(port[:-1])
            client_log.info(f'set default {host_} [{port}]')
            return host, port
        except ValueError:
            client_log.info(f'no arguments. set default {host_} [{port_}]')
            return host_, port_
    else:
        client_log.info(f'no arguments. set default {host_} [{port_}]')
        return host_, port_


def main(params):
    host = params[0]
    port = params[1]

    while True:
        try:
            '''
            TODO: Тут вставить разбор, например, если ответ существует, то уже не посылать пресенсе...
            '''
            presence = {"action": "presence", "ip": "ip"}
            client = Client(host, port)
            client.send_request(presence)
            response = client.parse_response(client.get_response())
            request = {"action": "broadcast_message", "message": response}
            client.send_request(request)
        except KeyboardInterrupt:
            server_log.info('Ctrl+C detected. Exit.')
            sys.exit()


if __name__ == '__main__':
    client_log.debug(f'Application initialization...')
    main(cmd_client(sys.argv))