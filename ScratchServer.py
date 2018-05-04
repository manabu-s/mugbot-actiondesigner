#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import socketserver
except:
    import SocketServer as socketserver
import signal
import socket
import serial
import os
import json
import sys

HOST, PORT = '0.0.0.0', 51234
serial = serial.Serial('/dev/ttyACM0',  57600)

class ScratchHandler(socketserver.BaseRequestHandler):
    def setup(self):
        os.system('/home/pi/mugbot-talk-1.1.sh ' + 'スクラッチとの接続を開始しました &')
        # for speak in English
        # os.system('espeak -ven+f3 -k5 -s150 "Scratch connection established" &')
        
    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            if len(self.data) == 0:
                break
            json_obj = json.loads(self.data)
            action = json_obj['action']
            arg = json_obj['arg']
            if action == 'face_y':
                arg = min(max(int(arg) + 95, 80), 110)
                serial.write((str(arg) + 'y').encode())
            elif action == 'face_x':
                arg = min(max(int(arg) + 90, 5), 175)
                serial.write((str(arg) + 'x').encode())
            elif action == 'eye':
                arg = min(max(int(arg), 0), 255)
                serial.write((str(arg) + 'z').encode())
            elif action == 'speech':
                serial.write('t'.encode())
                if sys.version_info.major == 2:
                    arg = arg.encode('utf-8')
                os.system('/home/pi/mugbot-talk-1.1.sh ' + arg + ' &')
                # for speak in English
                # os.system('espeak -ven+f3 -k5 -s150 ' + '"' + arg +'" &')
                serial.write('n'.encode())
            else:
                print('Unknown Command')
            
class ScratchServer(socketserver.ThreadingTCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.socket.bind(self.server_address)
        
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    server = ScratchServer((HOST, PORT), ScratchHandler)
    server.serve_forever()
