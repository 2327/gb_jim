#!/usr/bin/env python3

import sys
import socket
from tests.tests import *
from client.client_log_config import *
from common.jim_log import *
from common.config import *


@decolog
def cmd_client(params):
    '''
    TODO: need to add log options for foreground and verbose
          nedd add ConfigParser for working with config file
    '''

    host_, port_ = HOST, PORT

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


@decolog
def main(params):
    host, port = params[0], params[1]

    while True:
        presence = {"action": "presence", "ip": "ip"}
        client = Client(host, port)
        client.send_request(presence)
        print(client.get_response())
        time.sleep(2)
        '''
        message = input('Enter your message: ')
        if message:
            request = {"action": "broadcast_message", "message": message}
            client.send_request(request)
        '''
class Client:
    def __init__(self, host, port):
        self.address = (host, port)
        self.sock = socket.socket()
        self.sock.settimeout(1)

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
        client_log.debug(f'Successfully send message: {byte_request}')

    @decolog
    def get_response(self, size=SIZE):
        try:
            byte_response = self.sock.recv(size)
            client_log.debug(f'Successfully receive response: {byte_response}')
            response = convert(byte_response)
        except OSError:
            response = ''
            print(f'get_response: {response}')
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


if __name__ == '__main__':
    main(cmd_client(sys.argv))