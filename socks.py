#!/usr/bin/env python3

import socket
import ssl

class Socks:
    
    def __init__(self, addr, user):
        self.addr = addr
        self.user = user
    
    def create_connection(self, addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = ssl.wrap_socket(s, ca_certs="server.crt", cert_reqs=ssl.CERT_REQUIRED)
        conn.connect(self.addr)
        conn.send(bytes('CONNECT '+str(addr[0])+' '+str(addr[1])+' '+self.user+'\r\n', 'utf8'))
        return conn


if __name__ == '__main__':
    socks = Socks(('localhost', 9999), 'student')
    #socks = Socks(('staff.tcs.uj.edu.pl', 9999), 'student')
    
    connection = socks.create_connection(('bot.whatismyipaddress.com', 80))
    connection.send(bytes('GET / HTTP/1.1\r\nHost: bot.whatismyipaddress.com\r\nConnection: close\r\n\r\n', 'ascii'))
    rfile = connection.makefile('rb')
    print(rfile.read())
