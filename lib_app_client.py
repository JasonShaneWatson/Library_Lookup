#!/usr/bin/python
# -*- coding: utf-8 -*-

# Jason Watson

####
# User Client
# The Client program needs to read multiple book titles from a JSON-file called “input.json”. For each book in this
# file it sends a query to the "Librarian" server asking for its status. Before send the query, the program
# must send a hello message. The program can send the query after receiving hello response.
# After it receives the book status from the server
# it writes the book title, author, and status in another JSON-file called “output.json”. In case a book is borrowed it
# must write additionally the name of the person who borrowed the book, their email address and phone number, and
# the date that the book will be returned to the library. Each book lookup must be over a new TCP connection.
###

import socket
import json
import sys
from time import sleep

if sys.version_info[0] < 3:
    sys.exit('Python version 3 or greater is required to run this program'
             )

serverIP = 'localhost'
serverPort = 47470
maxBuffSize = 4096  # https://docs.python.org/3/library/socket.html
debug = False  # set to true for verbose process logging

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    fileName = ''

    # if we were passed a parameter and the parameter ends in .json, use that for the fileName

    if sys.argv and len(sys.argv) > 1 and (sys.argv[1])[-5:] == '.json':
        fileName = sys.argv[1]
    else:
        if debug:
            print('Input file name not passed as parameter. Defaulting to input.json')
        fileName = 'input.json'

     # load input file that will have list of books to query

    bookRequests = ''
    try:
        f = open(fileName, 'r')
        bookRequests = f.read()
        bookRequests = json.loads(bookRequests)
        f.close()
    except Exception as e:
        print("Exception",e)
        sys.exit("Couldn't read from the input file.")

    # loop through each book in the input file and use a TCP socket to query information from the librarian server

    bookQuery = {'Title': 'BookInquiry'}
    allResults = []
    for book in bookRequests['Query']:
        try:
            bookQuery['BookName'] = '{}'.format(book['Book title'])
            helloMsg = {'Title': 'Hello', 'Sender': 'userClient'}

            # make and connect a TCP connection with the server

            sock = ConnectSocket(serverIP, serverPort)
            SendTCPMessage(sock, json.dumps(helloMsg))
            result = SendTCPMessage(sock, json.dumps(bookQuery))
            result = json.loads(result)

            # if the book is borrowed, lookup phone and email of the person who has it

            if 'Status' in result.keys() and result['Status'] \
                == 'Borrowed':
                userQuery = {'Title': 'UserInquiry'}
                userQuery['UserName'] = result['BorrowedBy']
                userInfo = SendTCPMessage(sock, json.dumps(userQuery))
                userInfo = json.loads(userInfo)

                # if request returned a user, add that info to the output, Skip name because that is already in BorrowedBy

                if 'Name' in userInfo.keys():
                    for item in userInfo.keys():
                        if item != 'Name':
                            result[item] = userInfo[item]
                elif 'Error' in userInfo.keys() or 'Alert' \
                    in userInfo.keys():
                    for item in userInfo.keys():
                        result[item] = userInfo[item]

            # print the book query results

            for item in result.keys():
                print('{}:{}'.format(item, result[item]))
            print('')
            allResults.append(result)
        except Exception as e:
            print("Exception",e)
        finally:
            sock.close()
    try:

        # write the Output file

        f = open('output.json', 'w')
        formattedResults = '[\n'
        for item in allResults:
            formattedResults += '    {\n'
            for key in item.keys():
                formattedResults += '        "{}":"{}",\n'.format(key,
                        item[key])

            # remove comma from last item in object

            formattedResults = formattedResults[:-2]
            formattedResults += '\n'
            formattedResults += '    },\n'

        # remove comma from last object

        formattedResults = formattedResults[:-2]
        formattedResults += '\n'
        formattedResults += ']'
        f.write(formattedResults)
        f.close()
    except Exception as e:
        print('Error writing results to output.json')
        print("Exception",e)


####
# Create a tcp connection
###

def ConnectSocket(ip, port):

    # Create a TCP/IP socket

    try:
        s = socket.create_connection((ip, port))
    except:
        print("Error creating TCP socket connection. Trying Again...\nMake sure the 'Librarian' server is running.")
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
    if debug:
        print('sending "%s"' % msg)
    try:
        sock.sendall(msg.encode())
        data = sock.recv(maxBuffSize).decode()
        if debug:
            print('received "%s"' % data)
        response = data
    except Exception as e:
        print("Exception",e)
    return response

main()
