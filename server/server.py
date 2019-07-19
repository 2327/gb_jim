import os
import sys
import select
import socket
from tests.tests import *
from client.client_log_config import *
from server.server_log_config import *
from common.jim_log import *
from common.config import *

clients, collected_responses = [], []

class Server:
    def __init__(self, host, port, que=5):
        self.address = (host, port)
        self.sock = socket.socket()
        self.sock.setblocking(False)
        self.sock.settimeout(0.2)
        self.sock.bind(self.address)
        self.sock.listen(que)

    def make_response(self, request):
        server_log.debug(f'Received request {request}')
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
                response = self.make_response(convert(byte_request))
                collected_responses.append(response)
                print('1', collected_responses)

                return collected_responses
            except:
                server_log.debug(f'Sender {client} was disconnected.')
                clients.remove(client)

            collected_responses.append(response)

            return collected_responses

    def get_request(self, client):
        try:
            byte_request = client.recv(SIZE)
        except socket.error:
            server_log.debug(f'Socket error {client}')
            byte_request = None
        return byte_request

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
                server_log.debug(f'Send response')
                clients_rx.remove(client)
            except:
                ip_ = client.getpeername()
                print(f'Reader was {ip_} disconnected.')
                clients_rx.remove(client)
        #        collected_responses = []
        return True

    def main_loop(self):
        while True:
            try:
                client, addr = self.sock.accept()
                ip_ = client.getpeername()
                server_log.debug(f'Connected from {ip_}')
                request = convert(self.get_request(client))
                server_log.debug(f'Received message: {request}')
                response = self.make_response(request)
                self.send_response(client, response)
                server_log.debug(f'Send presence {response}')

            except OSError as e:
                pass
            else:
                clients.append(client)
            finally:
                wait = 0
                clients_rx = []
                clients_tx = []

                try:
                    clients_tx, clients_rx, e = select.select(clients, clients, [], wait)
                except:
                    pass


                collected_requests = self.get_requests(clients_tx, clients)
                if collected_requests:
                    print(collected_requests)
                self.send_responses(clients_rx, collected_requests)
