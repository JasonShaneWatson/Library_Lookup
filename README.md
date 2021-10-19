# Library\_Lookup
Book queries utilizing TCP sockets

## Description
This project consists of four programs: lib\_app\_bookSrv.py(book server), lib\_app\_userSrv.py(user server), lib\_app\_librarian.py(librarian server), and lib\_app\_client.py(client app). The 4 programs together create a library application that can be supplied with a JSON input file of book names and it will return information about each book.

## To run the project:
* Execute run\_app.bat and follow the instructions for usage that are printed.

or

* Open 4 command prompts. Start each server with: python3 lib\_app\_servername.py
* In the last command prompt execute the client application:
    * Usage: python3 lib\_app\_client.py "<inputFile>"


## Troubleshooting
if a port is already in use on your machine, you can modify the port for that program. Each program defines a global variable at the top that specifie s the port. If you change the port for a server, be sure you change the port in the client program as well.
* Server: lib\_app\_librarian.py
    *Client: lib_app_client.py
* Server: lib\_app\_userSrv.py or lib\_app\_bookSrv.py
    *Client: lib_app_librarian.py


## Each lookup consists of the following:
1. The client server sends a hello message to the librarian server.
2. The librarian server sends a welcome message.
3. The client sends a BookInquiry to the librarian server.
4. The librarian server forwards the query to the book server.
5. The book server receives the query, looks up the book, and responds with pertinent info.
6. The librarian server forwards the answer to the client.
7. If  the book Status is borrowed, the client sends a UserInquiry to the librarian server.
8. The librarian server forwards the query to the user server.
9. The user server receives the query, looks up the user, and responds with pertinent info.
10. The librarian server forwards the answer to the client.
11. The client prints the details of the book and optional user query to the screen. 
12. After all queries are made, the client will write them to a file in the current directory named “output.json”.

