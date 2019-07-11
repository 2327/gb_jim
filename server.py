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
        self.sock.settimeout(0.2)

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
#            try:
#                ip_
#            except KeyboardInterrupt:
#                self.sock.close()
#                server_log.info('Ctrl+C detected. Exit.')
#                sys.exit()
#            except:
            try:
                client, addr = self.sock.accept()
                print(f'10: {client}')
            except OSError as e:
                print('20:')
                pass
            else:
                clients.append(client)
                print(f'30: {clients}')
                ip_ = client.getpeername()
                server_log.info(f'Connected from {ip_}')
            finally:
               print('40:')
               clients_rx = []
               clients_tx = []
               wait = 10
#
#                try:
#                    clients_rx, clients_tx, e = select.select([], clients, [], wait)
#                except Exception as e:
#                    pass
#
            print(f'50: {clients_tx}')
#
#                for client_tx in clients_tx:
#                    timestr = time.ctime(time.time()) + "\n"
#
#                print(f'3.1: {client_tx}')

#                try:
#                    client_tx.send(timestr.encode('utf-8'))
#                except:
#                     clients_tx.remove(client_tx)

#                print('4: ', clients_rx, clients_tx, e)
#
#                if len(clients_tx) > 0:
#                    print('5: ')
#                    byte_request = self.get_request(clients_tx)
#                    print('6: ')
#                    response = self.make_response(byte_request)
#                    print(f'7: {response}')
#                    self.send_response(clients_rx, response)
#                    server_log.info(f'Send response {response}')

#                '''
#                TODO: make event for close socket
#                client.close()
#                '''

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
    server_log.info(f'no arguments. set default {host} [{port}]')
    server.main_loop()

if __name__ == '__main__':
    server_log.debug('Application initialization...')
    main(cmd_server(sys.argv))
