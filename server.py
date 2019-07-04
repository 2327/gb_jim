#!/usr/bin/env python3

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
        print(request)
        return byte_request

    def send_response(client, response):
        byte_response = convert(response)
        print(byte_response)
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
        print(byte_response)
        client_sock = client.getpeername()
        try:
            client.send(byte_response)
            client.close()
            return True
        except socket.error:
            print('Failed to send, IP: {}'.format(client_sock[1]))

    def main_loop(self):
        count = 1
        while True:
            try:
                client, addr = self.sock.accept()
                print('connected {}'.format(client.getpeername()))
                byte_request = self.get_request(client)
                response = self.make_response(byte_request)
                self.send_response(client, response)
                count += 1
                client.close()
            except KeyboardInterrupt:
                print('\n', 'exit')
                self.sock.close()
                sys.exit()


def cmd_server(params):
    '''
    Тут сделать обработку параметров командной строки
    '''
    host = HOST
    port = PORT
    return host, port

def main(params):
    host = params[0]
    port = params[1]
    server = Server(host, port)
    logging.info('no arguments. set default ' +  host + '['+ str(port) + ']')
    server.main_loop()

if __name__ == '__main__':
    ''' 
    test_actual_time()
    test_convert_empty()
    test_convert_dict()
    '''
    logging.debug('Application initialization...')
    main(cmd_server(sys.argv))
