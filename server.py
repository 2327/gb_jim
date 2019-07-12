#!/usr/bin/env python3

import os
import sys
import select
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
        self.sock.setblocking(1)
        self.sock.settimeout(0.05)

    def get_request(self,client):
        byte_request = client.recv(SIZE)
        request = convert(byte_request)
        server_log.info(f'Received message: {request}')
        return byte_request

    def make_response(self, byte_request):
        request = convert(byte_request)
        server_log.info(f'Received request {request}')
        if 'action' in request and request['action'] == 'presence':
            response = {"response": 200,"time": time.time()}
        elif 'action' in request and request['action'] == 'broadcast_message':
            response = {"response": 200, "time": time.time(), "message": request['message']}
        return response

    def send_response(self, client, response):
        byte_response = convert(response)
        client_sock = client.getpeername()
        ip_ = client_sock[1]
        try:
            client.send(byte_response)
            server_log.info(f'Successfully send message. Client: {client_sock}')
            '''
            client.close()
            '''
            return True
        except socket.error:
            server_log.info(f'Failed to send message. Client: {client_sock}')

    def main_loop(self):
        clients = []

        while True:
            try:
                client, addr = self.sock.accept()
                ip_ = client.getpeername()
                server_log.info(f'Connected from {ip_}')
            except OSError as e:
                pass
            else:
                clients.append(client)
            finally:
                wait = 1
                clients_rx = []
                clients_tx = []


            try:
                clients_rx, clients_tx, e = select.select(clients, clients, [], wait)
            except:
                pass

            if clients_tx:
                for client in clients_tx:
                    byte_request = self.get_request(client)
                    response = self.make_response(byte_request)
                    self.send_response(client, response)

            print('end')


#            if clients_rx:
#                for client in clients_rx:
#                    response = self.make_response(byte_request)
#                    self.send_response(client, response)
#                    server_log.info(f'Send response {response}')
#                    client.close()

def cmd_server(params):
    '''
    TODO: need to add log options for foreground and verbose
          nedd add ConfigParser for working with config file
    '''
    host = HOST
    port = PORT
    return host, port

def main(params):
    host, port = params[0], params[1]
    server = Server(host, port)
    server_log.info(f'no arguments. set default {host} [{port}]')
    server.main_loop()

if __name__ == '__main__':
    server_log.debug('Application initialization...')
    main(cmd_server(sys.argv))
