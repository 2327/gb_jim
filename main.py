#!/usr/bin/env python3

import os
import sys
import select
import socket
from tests.tests import *
from client.client_log_config import *
from client.client import *
from server.server_log_config import *
from server.server import *
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
    host, port, mode, c = params[0], params[1], params[2], 0

    if mode == 'client':
        while True:
            try:
                presence
                request = {"action": "broadcast_message", "client": client_name, "message": c}
                client.send_request(request)
                print(client.get_response())
                c += 1
            except:
                presence = {"action": "presence", "client": client_name}
                client = Client(host, port)
                client.send_request(presence)
                if response['response'] == 200:
                    read = threading.Thread(target=client.get_response, args=())
                    read.start()
                print('MSG: ', client.get_response())
    elif mode == 'read':
        client_name = input('Enter your name or \'enter\' for anonymous: ')
        if client_name == '':
            client_name = random.randint(1, 101)

        client = Client(host, port, client_name)
        client.get_connect()

        try:
            presence
        except:
            client.send_request('presence')
            print(client.get_response())
            presence = '0'

        time.sleep(0.1)
        client.send_request('get_contacts')
        print(client.get_response())

#        while True:
#            print(client.get_response())
#
#            read = threading.Thread(target=client.get_response, args=())
#            read.start()
#            read.join()
#            time.sleep(1)
#
#            c += 1

    elif mode == 'write':
        client_name = input('Enter your name or \'enter\' for anonymous: ')
        if client_name == '':
            client_name = random.randint(1, 101)
        while c < 30:
            request = {"action": "broadcast_message", "client": client_name, "message": c}
            client = Client(host, port, client_name)
            client.get_connect()
            try:
                presence
            except:
                client.send_request('presence')
                client.get_response()
                presence = '0'

            client.send_request('get_contacts')
            print(client.get_response())
            client.send_request(request)
            print(client.get_response())
            c += 1
        else:
            exit(0)
    else:
        database = Storage()
        server = Server(host, port, database)
        server_log.info(f'no arguments. set default {host} [{port}]')
        server.main_loop()

if __name__ == '__main__':
    server_log.debug('Application initialization...')
    main(cmd_parseargs(sys.argv))
