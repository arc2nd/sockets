#!/usr/bin/python

from socket import *

serverName = 'gully'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('Input lowercase sentence: ')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('From Server: {}'.format(modifiedSentence.decode()))
clientSocket.close()


