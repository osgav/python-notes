#!/usr/bin/env python

import SocketServer
import socket

class EchoHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        
        print "Got Connection from: ", self.client_address
        data = 'dummy'

        while len(data):
            data = self.request.recv(1024)
            print "Client sent: " + data
            self.request.send(data)

        print "Client left"


# define a server IP and port in a tuple
serverAddr = ("0.0.0.0", 9000)

# create a TCP Server, passing in the server address tuple, and 
# a class which will handle all clients connecting to the server
server = SocketServer.TCPServer(serverAddr, EchoHandler)

# run forever and process as many clients as possible
server.serve_forever()


