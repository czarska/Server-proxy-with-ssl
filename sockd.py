#!/usr/bin/env python3

import socket
import socketserver
import struct
import select
import ssl
from threading import Thread

PORT=9999

class MainHandler(socketserver.StreamRequestHandler):
    
    def create_connection(self):
        conn = socket.create_connection((self.host, self.portt))
        return conn

    def parse(self,str):
        s = str.split(" ")
        self.host = s[1]
        self.portt = s[2]
        self.username = s[3]

    def reading(self):
        while self.eof == 0:
            a,b,c = select.select([self.rfile, self.rf],[],[])
            if self.rfile in a:
                str = self.rfile.read1(2048)
                if str == bytes(0):
                    self.eof = 1
                else:
                    self.wf.write(str)
                    self.wf.flush()
    
            if self.rf in a:
                str = self.rf.read1(2048)
                if str == bytes(0):
                    self.eof = 1
                else:
                    self.wfile.write(str)
                    self.wfile.flush()
        self.connection.close()
        self.request.close()


    def handle(self):
        
        #Reading and parsing first (header) line
        line = self.rfile.read1(2048)
        ll = (line.decode('utf-8')).split('\n')
        self.data = ll[0]
        l = '\n'.join(ll[1:])
        self.parse(self.data)
        
        #Creating new connection (with 2)
        self.connection = self.create_connection()
        
        #Create files for 2
        self.rf = self.connection.makefile('rb')
        self.wf = self.connection.makefile('wb')
        
        #Rewriting rest of read part
        self.wf.write(bytes(l, 'ascii'))
        self.wf.flush()

        #Reading
        self.eof = 0
        self.reading()


class MainServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    def __init__(self, addr=('', PORT), certfile="server.crt", keyfile="server.key", ssl_version=ssl.PROTOCOL_TLSv1):
        super().__init__(addr, MainHandler)
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version
    def get_request(self):
        newsock, addrr = self.socket.accept()
        connn = ssl.wrap_socket(newsock, server_side=True, certfile = self.certfile, keyfile = self.keyfile, ssl_version = self.ssl_version)
        return connn, addrr

if __name__ == '__main__':
    server = MainServer()
    server.serve_forever()
