#!/usr/bin/python

import struct
import socket

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect((host, port))


def sendMessage(host=None, port=None, sock=None, msg=None):
    if not sock:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print('making connection to: {}\nport: {}'.format(host, port))
    try:
        msg = struct.pack('>i', len(msg)) + msg
        print('packed: {}'.format(msg))
        sock.sendall(msg)

        #look for response
        amt_rcvd = 0
        amt_expected = len(msg) - 4

        while amt_rcvd < amt_expected:
            data = sock.recv(16)
            amt_rcvd += len(data)
            print('received: {}'.format(data))
    finally:
        print('closing socket')
        sock.close()
