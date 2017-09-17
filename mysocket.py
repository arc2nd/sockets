#!/usr/bin/python
#James Parks
#09/11/17

import sys
import struct
import socket
from optparse import OptionParser

def parse_args(all_args):
    parser = OptionParser(version = '%prog 1.0')
    parser.add_option('-s', '--server', action='store_true', help='run as server')
    parser.add_option('-c', '--client', action='store_true', help='run as client')

    options, args = parser.parse_args(all_args)
    return options, args

class mysocket:
    def __init__(self, sock=None, host=None, port=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.host = host
        self.port = port
        self.verbosity = 1

    def _log(self, priority, comment):
        if self.verbosity >= priority:
            print comment

    def connect(self):
        self.sock.connect((self.host, self.port))
        self._log(1, 'making connection to: {}\nport: {}'.format(self.host, self.port))

    def sendMessage(self, sock=None, msg=None):
        try:
            msg = struct.pack('>i', len(msg)) + msg
            self._log(6, 'packed: {}'.format(msg))
            sock.sendall(msg)

            # look for ack
            isAck = self.recv_msg(sock)
            if isAck == 'ack':
                self._log(3, 'message receipt acknowledged')
            else:
                self._log(1, 'message receipt un-ack: {}'.format(isAck))
        finally:
            self._log(1, 'closing socket')
            self.sock.close()

    def recv_msg(self, sock):
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>i', raw_msglen)[0]
        return self.recvall(sock, msglen)

    def recvall(self, sock, n):
        data = ''
        chunks = []
        while len(data) < n:
            chunk = sock.recv(n - len(data))
            chunks.append(chunk)
            if not chunk:
                return None
            data = ''.join(chunks)
        #data = ''.join(chunks)
        self._log(1, data)
        return data

    """def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_rect < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError('socket connection broken')
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)
    """

    def serve(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)

        while True:
            # accept connections from outside
            (clientsocket, address) = self.sock.accept()
            # do soemthing with the clientsocket
            try:
                chunks = []
                self._log(1, 'connection from: {}'.format(address))
                # while True:
                msg = self.recv_msg(clientsocket)
                self._log(1, 'msg rcvd: {}'.format(msg))
                clientsocket.sendall(msg)
                self.sendMessage(sock=clientsocket, msg='ack')
                self._log(1, 'sending ack to client')
            finally:
                clientsocket.close()

if __name__ == '__main__':
    options, args = parse_args(sys.argv[1:])
    host = '192.168.0.2'
    port = 50007
    mys = mysocket(host=host, port=port)
    if options.server:
        mys.serve()



