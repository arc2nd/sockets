import os
import time
import json
import socket
import argparse


def my_parse():
    parser = argparse.ArgumentParser(version = '%prog 1.0')
    parser.add_argument('-s', '--server', dest='server', action='store_true', help='run as server')
    parser.add_argument('-c', '--client', dest='client', action='store_true', help='run as client')
    parser.add_argument('-a', '--addr', dest='addr', help='the address to send to')
    parser.add_argument('-p', '--port', dest='port', help='the port number')

    args = parser.parse_args()
    return args

def read_config(config_path='config.json'):
    config_dict = {}
    if os.path.exists(config_path):
        with open(config_path, 'r') as fp:
            config_dict = json.load(fp)
    return config_dict

def rx_packet(port):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(('', port))
    print('The server is ready to recieve')
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        now = time.time()
        print('MSG: {}\tRX: {}\tDIFF: {}'.format(message, now, (now-float(message))))
    return

def tx_packet(addr, port):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = str(time.time())
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    clientSocket.sendto(message.encode(), (addr, port))
    clientSocket.close()
    return

if __name__ == '__main__':
    args = my_parse()
    server = args.server
    client = args.client
    config_dict = read_config()
    if server:
        rx_packet(config_dict['port'])
    elif client:
        tx_packet(config_dict['addr'], config_dict['port'])
