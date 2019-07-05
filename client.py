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

class Client:
    def __init__(self, host, port):
        self.address = (host, port)
        self.sock = socket.socket()
        self.sock.connect(self.address)

        try:
            self.sock.connect(self.address)
        except socket.error:
            try:
                client_log.info('Coldn\'t connect to server...')
                time.sleep(1)
            except KeyboardInterrupt:
                client_log.info('Ctrl+C detected. Exit.')
                print('\n', 'Ctrl+C detected. Exit.')
                self.sock.close()
                sys.exit()
        except KeyboardInterrupt:
            client_log.info('Ctrl+C detected. Exit.')
            print('\n', 'Ctrl+C detected. Exit.')
            self.sock.close()
            sys.exit()

    def send_request(self, request):
        byte_request = convert(request)
        self.sock.send(byte_request)

    def get_response(self, size=SIZE):
        byte_response = self.sock.recv(size)
        response = convert(byte_response)
        self.sock.close()
        return response

    def parse_response(self, response):
        code = response['response']
        time_ = act_time(response['time'])
        return 'code: {} - {}, time: {}'.format(code, CODES[code], time_)

def cmd_client(params):
    host_ = HOST
    port_ = PORT

    if len(params) == 2:
        try:
            host, port = params[1].split('[')
            port = int(port[:-1])
            client_log.info('set default 127.0.0.1[', port, ']')
            return host, port
        except ValueError:
            client_log.info('set default 127.0.0.1[7777]')
            return host_, port_
    else:
        client_log.info('no arguments. set default ' +  host_ + '['+ str(port_) + ']')
        return host_, port_


def main(params):
    host = params[0]
    port = params[1]
    presence = {"action": "presence", "2": "2"}

    client = Client(host, port)
    client.send_request(presence)
    response = client.get_response()
    client_log.info(client.parse_response(response))

if __name__ == '__main__':
    client_log.debug('Application initialization...')
    main(cmd_client(sys.argv))