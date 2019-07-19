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
import argparse
import subprocess


HOST = '127.0.0.1'
PORT = 7777
SIZE = 1024
CODING = 'utf-8'
MODE = 'client'


class Client:                                                                                                                                                                                                                    
    def __init__(self, host, port):                                                                                                                                                                                              
        self.address = (host, port)                                                                                                                                                                                              
        self.sock = socket.socket()
        self.sock.setblocking(True)
        self.sock.settimeout(1.0)
                                                                                                                                                                                                                                 
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
        client_log.debug(f'Successfully sent message: {byte_request}')
                                                                                                                                                                                                                                 
    @decolog                                                                                                                                                                                                                     
    def get_response(self, size=SIZE):
        try:
            byte_response = self.sock.recv(size)                                                                                                                                                                                 
#            client_log.debug(f'Successfully receive response: {byte_response}')
##            response = convert(byte_response)
            response = byte_response
        except OSError:
            response = ''                                                                                                                                                                                                        
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


class Server:
    def __init__(self, host, port, que=5):
        self.address = (host, port)                                                                                                                                                                                              
        self.sock = socket.socket()                                                                                                                                                                                              
        self.sock.setblocking(True)
        self.sock.settimeout(0.2)
        self.sock.bind(self.address)                                                                                                                                                                                             
        self.sock.listen(que)           

    def get_request(self, client):
        try:
            byte_request = client.recv(SIZE)
            request = convert(byte_request)
            server_log.info(f'Received message: {request}')
            return byte_request
        except socket.error:
            server_log.info(f'Socket error {client}')
            pass

    def make_response(self, byte_request):
        request = convert(byte_request)
        server_log.info(f'Received request {request}')
        if 'action' in request and request['action'] == 'presence':
            response = {"response": 200, "time": time.time(), "action": request['action']}
        elif 'action' in request and request['action'] == 'broadcast_message':
            response = {"response": 200, "time": time.time(),
                        "action": request['action'], "message": request['message']}
        else:
            if request:
                response = {"response": 200, "time": time.time(),
                            "action": "error", "message": request}
            else:
                response = {"response": 200, "time": time.time(),
                            "action": "error", "message": "empty"}
        return response

    def get_requests(self, clients_tx, clients):
        for client in clients_tx:
            try:
                byte_request = self.get_request(client)
                if isinstance(byte_request, bytes):
                    response = self.make_response(byte_request)
                    collected_responses.append(dict(response), client)
            except:
                print(f'Sender {client} was disconnected.')
                clients.remove(client)
                clients_tx.remove(client)

    def send_response(self, client, responses):
        byte_response = convert(responses)
        try:
            client.send(byte_response)
        except socket.error:
            print('socket error')
            pass

        return True  

    def send_responses(self, clients_rx, collected_requests):
        for client in clients_rx:
            try:
                self.send_response(client, collected_requests)
                server_log.info(f'Send response')
                clients_rx.remove(client)
            except:
                ip_ = client.getpeername()
                print(f'Reader was {ip_} disconnected.')
                clients_rx.remove(client)
#        collected_responses = []
        return True

    def main_loop(self):
        clients, collected_responses = [], []

        while True:                                                                                                                                                                                                              
            try:                                                                                                                                                                                                                 
                client, addr = self.sock.accept()                                                                                                                                                                                
                if client:                                                                                                                                                                                                       
                    ip_ = client.getpeername()                                                                                                                                                                                   
                    server_log.info(f'Connected from {ip_}')
                    byte_request = self.get_request(client)
                    response = self.make_response(byte_request)
                    self.send_response(client, response)
                    server_log.info(f'Send presence {response}')
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

            collected_requests = self.get_requests(clients_tx, clients)
            self.send_responses(clients_rx, collected_requests)


@decolog
def cmd_parseargs(params):
    '''
    TODO: need to add log options for foreground and verbose
          nedd add ConfigParser for working with config file
    '''
    parser = argparse.ArgumentParser(description='JIM: my first messanger')
    parser.add_argument('--verbose', help='verbose')
    parser.add_argument('--host', action='store',  help='bind address')
    parser.add_argument('--port', action='store', help='bind port')
    parser.add_argument('--mode', action='store', help='mode')
    args = parser.parse_args()
    if args.verbose:
        print('verbose mode')

    if args.host == '127.0.0.1':
        HOST = args.host
        client_log.info(f'set default {HOST}')
    else:
        HOST = '127.0.0.1'

    if args.host == 7777:
        PORT = args.port
        client_log.info(f'set default {PORT}')
    else:
        PORT = 7777

    if args.mode == 'server' or args.mode == 'read' or args.mode == 'write':
        MODE = args.mode
    else:
        MODE = 'client'

    host, port, mode = HOST, PORT, MODE

    return host, port, mode


@decolog
def main(params):
    host, port, mode = params[0], params[1], params[2]

    c = 0
    if mode == 'client':
        while c < 10:
            try:
                presence
                request = {"action": "broadcast_message", "message": c}
                client.send_request(request)
                print(client.get_response())
                c += 1
            except:
                presence = {"action": "presence", "ip": "ip"}
                client = Client(host, port)
                client.send_request(presence)
                print('MSG: ', client.get_response())
    elif mode == 'read':
        while c < 10:
            client = Client(host, port)
            print('Message: ', client.get_response())
            c += 1
    elif mode == 'write':
        while c < 10:
            request = {"action": "broadcast_message", "message": c}
            client = Client(host, port)
            client.send_request(request)
            c += 1
    else:
        server = Server(host, port)
        server_log.info(f'no arguments. set default {host} [{port}]')
        server.main_loop()

if __name__ == '__main__':
    server_log.debug('Application initialization...')
    main(cmd_parseargs(sys.argv))
