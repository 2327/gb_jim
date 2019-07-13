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
        self.sock.setblocking(0)
        self.sock.settimeout(1.0)
        self.sock.bind(self.address)
        self.sock.listen(que)


    def get_request(self, client):
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
        '''
        client_sock = client.getpeername()
        ip_ = client_sock[1]
        '''
        try:
            client.send(byte_response)
        except socket.error:
            pass
        return True

    def main_loop(self):
        clients = []

        while True:
            try:
                client, addr = self.sock.accept()
                if client:
                    ip_ = client.getpeername()
                    server_log.info(f'Connected from {ip_}')
            except OSError as e:
                pass
            else:
                clients.append(client)
            finally:
                wait = 0
                clients_rx = []
                clients_tx = []

            try:
                clients_rx, clients_tx, e = select.select(clients, clients, [], wait)
            except:
                pass

            print(f'WRITE: {clients_tx}, READ: {clients_rx}')

            for client in clients_tx:
                try:
                    byte_request = self.get_request(client)
                except:
                    print(f'Клиент отключился')
                    clients.remove(client)
                    clients_tx.remove(client)

            for client in clients_rx:
                try:
                    response = self.make_response(byte_request)
                    self.send_response(client, response)
                    server_log.info(f'Send response {response}')
                except:
                    ip_ = client.getpeername()
                    print(f'Клиент {ip_} отключился')
                    #                        clients.remove(client)
                    clients_rx.remove(client)


def cmd_server(params):
    '''
    TODO: need to add log options for foreground and verbose
          nedd add ConfigParser for working with config file
    '''
    host, port = HOST, PORT
    return host, port

def main(params):
    host, port = params[0], params[1]
    server = Server(host, port)
    server_log.info(f'no arguments. set default {host} [{port}]')
    server.main_loop()

if __name__ == '__main__':
    server_log.debug('Application initialization...')
    main(cmd_server(sys.argv))
