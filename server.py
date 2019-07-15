#!/usr/bin/env python3

import os
import sys
import select
import socket
from tests.tests import *
from client.client_log_config import *
from server.server_log_config import *
from common.jim_log import *
from common.config import *
import threading


HOST = '127.0.0.1'
PORT = 7777
SIZE = 1024
CODING = 'utf-8'


class Client:
    def __init__(self, host, port):
        self.address = (host, port)
        self.sock = socket.socket()

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
        byte_response = self.sock.recv(size)
        client_log.debug(f'Successfully receive response: {byte_response}')
        response = convert(byte_response)
        '''
        self.sock.close()
        client_log.debug(f'Socket was closed.')
        '''
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


class Server:
    def __init__(self, host, port, que=5):
        self.address = (host, port)
        self.sock = socket.socket()
        self.sock.setblocking(False)
        self.sock.settimeout(0.5)
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
                    try:
                        byte_request = self.get_request(client)
                        print('2')
                        response = self.make_response(byte_request)
                        print('3')
                        self.send_response(client, response)
                    except:
                        print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                        all_clients.remove(sock)


            print(clients_rx, clients_tx)


#            if clients_rx:
#                for client in clients_rx:
#                    response = self.make_response(byte_request)
#                    self.send_response(client, response)
#                    server_log.info(f'Send response {response}')
#                    client.close()


@decolog
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


def cmd_server(params):
    '''
    TODO: need to add log options for foreground and verbose
          nedd add ConfigParser for working with config file
    '''
    host, port, mode = HOST, PORT, client
    return host, port


def main(params):
    host, port = params[0], params[1]
    if mode == 'client':
        presence = {"action": "presence", "ip": "ip"}
        client = Client(host, port)
        client.send_request(presence)
        print(client.get_response())

        while True:
            '''
            response = raw_input('Enter your message: ')
            if response:
                request = {"action": "broadcast_message", "message": response}
                client.send_request(request)
            '''
            print(client.get_response())
            print('1')
    else:
        server = Server(host, port)
        server_log.info(f'no arguments. set default {host} [{port}]')
        server.main_loop()

if __name__ == '__main__':
    server_log.debug('Application initialization...')
    main(cmd_server(sys.argv))
