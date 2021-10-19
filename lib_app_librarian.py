#!/usr/bin/python
# -*- coding: utf-8 -*-

# Jason Watson

import socket
import sys
import json
from time import sleep

if sys.version_info[0] < 3:
    sys.exit('Python version 3 or greater is required to run this program'
             )

serverIP = 'localhost'
serverPort = 47470
bookSrvIP = 'localhost'
bookSrvPort = 47747
userSrvIP = 'localhost'
userSrvPort = 47477
maxBuffSize = 4096  # https://docs.python.org/3/library/socket.html

####
# starts listen() on serverIP:serverPort and enters infinite loop of waiting for connection, receiving data, and responding
###

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:

        # Bind the socket to the port

        server_address = (serverIP, serverPort)
        print('starting up on %s port %s' % server_address)
        sock.bind(server_address)

        # Listen for 1 incoming connections

        sock.listen(1)
        while True:

            # Wait for a connection

            print('waiting for a connection')
            (connection, client_address) = sock.accept()
            try:
                print('connection from', client_address)

                # Receive the data

                while True:
                    data = connection.recv(maxBuffSize).decode()
                    print('received "%s"' % data)
                    if data:
                        ProcessData(data, connection)
                    else:
                        break
            finally:

                # Clean up the connection

                connection.close()
    except Exception as e:
        print("Exception",e)
        sock.close()


####
# Will fetch data from helper servers depending on request
# data = decoded data from TCP message
# connection = the TCP connection that is used to reply from data returned from recv()
###

def ProcessData(data, connection):
    helloMsg = json.dumps({'Title': 'Hello', 'Content': 'Welcome'})
    recvdMsg = json.loads(data)
    title = recvdMsg['Title']
    if title == 'Hello':
        connection.sendall(helloMsg.encode())
    elif title == 'BookInquiry':

        # connection.sendall(0)

        sock = ConnectSocket(bookSrvIP, bookSrvPort)
        bookData = SendTCPMessage(sock, data)
        connection.sendall(bookData.encode())
    elif title == 'UserInquiry':
        sock = ConnectSocket(userSrvIP, userSrvPort)
        userData = SendTCPMessage(sock, data)
        connection.sendall(userData.encode())
    else:
        connection.sendall('"Title":"Error","Content":"Title must be one of Hello, BookInquiry, or UserInquiry"'.encode())
        connection.sendall(''.encode())  # close connection


####
# Create a tcp client connection
###

def ConnectSocket(ip, port):

    # Create a TCP/IP socket

    try:
        s = socket.create_connection((ip, port))
    except Exception as e:
        print("Exception",e)
        print('Error creating TCP socket connection with {} on port {}. Trying again'.format(ip,port))
        sleep(3)
        s = ConnectSocket(ip, port)
    return s


####
# Send a TCP message and return the response.
# socket = socket we will use to send TCP socket
# msg = decoded msg you want to send.
###

def SendTCPMessage(sock, msg):
    response = ''
    print('sending "%s"' % msg)
    try:
        sock.sendall(msg.encode())
        data = sock.recv(maxBuffSize).decode()
        print('received "%s"' % data)
        response = data
    except Exception as e:
        print(e)
    return response


main()
