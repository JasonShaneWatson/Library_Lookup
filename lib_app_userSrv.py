#!/usr/bin/python
# -*- coding: utf-8 -*-

# Jason Watson

import socket
import sys
import json

if sys.version_info[0] < 3:
    sys.exit('Python version 3 or greater is required to run this program'
             )

userSrvIP = 'localhost'
userSrvPort = 47477
maxBuffSize = 4096  # https://docs.python.org/3/library/socket.html
recievedHello = False


####
# starts listen() on userSrvIP:userSrvPort and enters infinite loop of waiting for connection, receiving data, and responding
###

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:

        # Bind the socket to the port

        server_address = (userSrvIP, userSrvPort)
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


def ProcessData(data, connection):

    # load json data into python variable

    requestedUser = json.loads(data)
    if 'Title' in requestedUser.keys() and 'UserName' \
        in requestedUser.keys() and requestedUser['Title'] \
        == 'UserInquiry':
        try:
            result = {}
            with open('Users.json') as userFile:
                users = json.load(userFile)

                # search through Books.json for the requested BookName

                for lookup in users['User']:
                    if lookup['Name'].lower() == requestedUser['UserName'].lower():
                        result['Name'] = '{}'.format(lookup['Name'].capitalize())
                        result['Email'] = ('{}'.format(lookup['Email']) if lookup['Email'] else 'Not Provided')
                        result['Phone'] = ('{}'.format(lookup['Phone']) if lookup['Phone'] else 'Not Provided')

                # if we found a result

                if 'Name' in result.keys():
                    connection.sendall(json.dumps(result).encode())
                else:
                    connection.sendall('{"Alert":"This user is not in the library database"}'.encode())
        except Exception as e:
            print("Exception",e)
            connection.sendall('{"Error":"Sorry the user server could not look up this user. Error 500"}'.encode())
    else:
        connection.sendall('{"Error":"Malformed user query"}'.encode())


main()
