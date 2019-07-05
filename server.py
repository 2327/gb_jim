#!/usr/bin/env python3

import os
import sys
import socket
from tests.tests import *
from server.server_log_config import *

HOST = '127.0.0.1'
PORT = 7777
SIZE = 1024
CODING = 'utf-8'


class Server:
    def __init__(self, host, port, que=5):
        self.address = (host, port)
        self.sock = socket.socket()
        self.sock.bind(self.address)
        self.sock.listen(que)

    def get_request(self,client):
        byte_request = client.recv(SIZE)
        request = convert(byte_request)
        server_log.info(f'Received message: {request}')
        return byte_request

    def send_response(client, response):
        byte_response = convert(response)
        server_log.info(f'Received message: {request}')
        client.send(byte_response)
        client.close()

    def make_response(self, byte_request):
        request = convert(byte_request)
        if 'action' in request and request['action'] == 'presence':
            response = {"response": 200,"time": time.time()}
            '''
            здесь должно быть формирование ответа
            '''
            return response

    def send_response(self, client, response):
        byte_response = convert(response)
        client_sock = client.getpeername()
        ip_ = client_sock[1]
        try:
            client.send(byte_response)
            server_log.info(f'Successfully send, IP: {ip_}')
            client.close()
            return True
        except socket.error:
            server_log.info(f'Failed to send, IP: {ip_}')

    def main_loop(self):
        count = 1
        while True:
            try:
                client, addr = self.sock.accept()
                ip_ = client.getpeername()
                server_log.info(f'connected {ip_}')
                byte_request = self.get_request(client)
                server_log.info(f'Received request {byte_request}')
                response = self.make_response(byte_request)
                self.send_response(client, response)
                server_log.info(f'Send response {response}')
                count += 1
                client.close()
            except KeyboardInterrupt:
                self.sock.close()
                server_log.info('Ctrl+C detected. Exit.')
                sys.exit()


def cmd_server(params):
    '''
    TODO: need to add log options for foreground and verbose
          nedd add ConfigParser for working with config file
    '''
    host = HOST
    port = PORT
    return host, port

def main(params):
    host = params[0]
    port = params[1]
    server = Server(host, port)
    server_log.info('no arguments. set default ' +  host + '['+ str(port) + ']')
    server.main_loop()

if __name__ == '__main__':
    server_log.debug('Application initialization...')
    main(cmd_server(sys.argv))
