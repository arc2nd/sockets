#!/usr/bin/python

import struct
import socket

host = socket.gethostname()
port = 50007
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5)

def recv_msg(sock):
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>i', raw_msglen)[0]
    return recvall(sock, msglen)

def recvall(sock, n):
    data = ''
    chunks = []
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        chunks.append(chunk)
        if not chunk:
            return None
        data = ''.join(chunks)
    #data = ''.join(chunks)
    print(data)
    return data

while True:
    #accept connections from outside
    (clientsocket, address) = serversocket.accept()
    #do soemthing with the clientsocket
    try:
        chunks = []
        print('connection from: {}'.format(address))
        #while True:
        msg = recv_msg(clientsocket)
        print('msg rcvd: {}'.format(msg))
        clientsocket.sendall(msg)
        print('sending data back to client')
            #chunk = clientsocket.recv(16)
            #if chunk:
            #    chunks.append(chunk)
                #print('received: {}'.format(data))
                #print('sending data back to the client')
            #    clientsocket.sendall(chunk)
            #else:
            #    print('no more data from: {}'.format(address))
            #    break
        #data = ''.join(chunks)
        #print('msg rcvd: {}'.format(data))
    finally:
        clientsocket.close()
