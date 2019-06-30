#!/usr/bin/env python3

import sys
import socket
from functions import *
import time
from tests import *

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
            return host, port
        except ValueError:
            print('set default 127.0.0.1[7777]')
            return host_, port_
    else:
        return host_, port_


def main(params):
    host = params[0]
    port = params[1]
    presence = {"action": "presence", "2": "2"}

    client = Client(host, port)
    client.send_request(presence)
    response = client.get_response()
    print(client.parse_response(response))

if __name__ == '__main__':
    main(cmd_client(sys.argv))