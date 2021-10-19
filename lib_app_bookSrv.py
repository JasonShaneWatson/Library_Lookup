#!/usr/bin/python
# -*- coding: utf-8 -*-

# Jason Watson

import socket
import sys
import json

if sys.version_info[0] < 3:
    sys.exit('Python version 3 or greater is required to run this program'
             )

bookSrvIP = 'localhost'
bookSrvPort = 47747
recievedHello = False
maxBuffSize = 4096  # https://docs.python.org/3/library/socket.html

####
# starts listen() on bookSrvIP:bookSrvPort and enters infinite loop of waiting for connection, receiving data, and responding
###

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:

        # Bind the socket to the port

        server_address = (bookSrvIP, bookSrvPort)
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

    requestedBook = json.loads(data)
    if 'Title' in requestedBook.keys() and 'BookName' \
        in requestedBook.keys() and requestedBook['Title'] \
        == 'BookInquiry':
        try:
            result = {}
            with open('Books.json') as bookFile:
                books = json.load(bookFile)

                # search through Books.json for the requested BookName

                for lookup in books['Books']:
                    if lookup['Book title'] and lookup['Book title'] == requestedBook['BookName']:
                        result['Title'] = '{}'.format(lookup['Book title'])
                        result['Author'] = ('{}'.format(lookup['Author']) if lookup['Author'] else 'Not Provided')
                        result['Status'] = ('{}'.format(lookup['Status']) if lookup['Status'] else 'Not Provided')
                        if lookup['Status'] == 'Borrowed':
                            result['BorrowedBy'] = \
                                ('{}'.format(lookup['BorrowedBy']) if lookup['BorrowedBy'] else 'Not Provided')
                            result['ReturnDate'] = \
                                ('{}'.format(lookup['ReturnDate']) if lookup['ReturnDate'] else 'Not Provided')

                # if we found a result

                if 'Title' in result.keys():
                    print('sending "%s"' % json.dumps(result))
                    connection.sendall(json.dumps(result).encode())
                else:

                # we didn't find the book, return a object with the book name and status blank as described in the instructions.

                    result['Title'] = requestedBook['BookName']
                    result['Status'] = ''
                    print('sending "%s"' % json.dumps(result))
                    connection.sendall(json.dumps(result).encode())
        except Exception as e:
            print('Exception', e)
            connection.sendall('{"Error":"Sorry the Book server could not look up this book. Error 500"}'.encode())
    else:
        connection.sendall('{"Error":"Malformed book query"}'.encode())

main()
