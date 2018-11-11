#!/usr/bin/env python

import threading
import SocketServer

class ThreadedEchoRequestHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		data = self.request.recv(1024)
		while len(data):
			# Echo back to the client
			cur_thread = threading.currentThread()
			response = '%s: %s' % (cur_thread.getName(), data)
			self.request.send(response)
			data = self.request.recv(1024)
		print "Client left"
		return

class ThreadedEchoServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

if __name__ == "__main__":

	import threading

	# configure the server address and pass into new instance
	# of ThreadedEchoServer 'server'
	address = ('localhost', 9000)  
	server = ThreadedEchoServer(address, ThreadedEchoRequestHandler)

	# Configure 'server' as a daemonized thread and start it
	server_thread = threading.Thread(target=server.serve_forever)
	#server_thread.setDaemon(True)  
	server_thread.start()
	print 'Server loop running in thread:', server_thread.getName()
	
	# this keeps the terminal open because server_thread.setDaemon backgrounds the process
	#server_thread.join()

	#server.socket.close()


