import os
import sys
import select
import socket
from tests.tests import *
from client.client_log_config import *
from server.server_log_config import *
from common.jim_log import *
from common.config import *
import sqlite3

clients, collected_responses = [], []
#sqlfile = os.path.join(os.path.dirname(__file__), "bazon.sqlite3")
sqlfile = "bazon.sqlite3"

class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(
                f'Попытка запуска с указанием неподходящего порта {value}. Допустимы адреса с 1024 до 65535.')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

class Storage:
    def __init__(self):
        conn = sqlite3.connect(sqlfile)
        cursor = conn.cursor()

    def register_new_client(self, client_id, ip):
        conn = sqlite3.connect(sqlfile)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO clients (login,information) VALUES (?,?)''', (client_id, ip))
        conn.commit()
        conn.close()

    def register_connect_client(self, client_id, activity, ip):
        conn = sqlite3.connect(sqlfile)
        cursor = conn.cursor()

        try:
            client_id = cursor.execute('''SELECT (login) FROM clients ORDER BY Name LIMIT 1''', client_id)
        except:
            self.register_new_client(client_id, ip)

        cursor.execute('''INSERT INTO logs (client_id, activity, ip) VALUES (?,?,?)''', (client_id, activity, ip))
        conn.commit()
        conn.close()

    def contact_list_add(self):
        pass

    def contact_list_remove(self):
        pass

    def contact_list_show(self):
        pass


class Server:
    def __init__(self, host, port, database, que=5):
        self.address = (host, port)
        self.database = database
        self.sock = socket.socket()
        self.sock.setblocking(False)
        self.sock.settimeout(0.2)
        self.sock.bind(self.address)
        self.sock.listen(que)

    def make_response(self, request, ip):
        server_log.debug(f'Received request {request}')
        if 'action' in request and request['action'] == 'presence':
            response = {"response": 200, "time": time.time(), "action": request['action']}
            self.database.register_connect_client(request['client'], response['time'], ip)
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

    def get_requests(self, clients_r, clients):
        for client in clients_r:
            try:
                byte_request = self.get_request(client)
                response = self.make_response(convert(byte_request))
                collected_responses.append(response)
                return collected_responses
            except:
                server_log.debug(f'Sender {client} was disconnected.')
                clients.remove(client)

            collected_responses.append(response)

            return collected_responses

    def get_request(self, client):
        try:
            byte_request = client.recv(SIZE)
            return byte_request
        except socket.error:
            server_log.debug(f'Socket error {client}')

    def send_response(self, client, responses):
        print(responses)
        byte_response = convert(responses)
        try:
            client.send(byte_response)
            collected_responses = []
        except socket.error:
            pass

        return True

    def send_responses(self, clients_rx, collected_requests):
        for client in clients_rx:
            try:
                self.send_response(client, collected_requests)
                server_log.debug(f'Send response')
                clients_rx.remove(client)
            except:
                clients_rx.remove(client)
        return True

    def main_loop(self):
        while True:
            try:
                client, addr = self.sock.accept()
                ip_ = client.getpeername()[0]
                '''
                ip_ = client.getpeername()
                request = convert(self.get_request(client))
                print('DDD: ', request)
                server_log.debug(f'Received message: {request}')
                response = self.make_response(request)
                self.send_response(client, response)
                server_log.debug(f'Send presence {response}')
                '''
            except OSError as e:
                pass
            else:
                server_log.debug(f'Connected from {ip_}')
                clients.append(client)
            finally:
                wait = 0
                clients_r = []
                clients_w = []
                try:
                    clients_r, clients_w, e = select.select(clients, clients, [], wait)
                except:
                    pass

                for client in clients_r:
                    request = convert(self.get_request(client))
                    if request != 'empty':
                        message = self.make_response(request, ip_)
                        collected_responses.append(message)
                self.send_responses(clients_w, collected_responses)
