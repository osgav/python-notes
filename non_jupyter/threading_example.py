#!/usr/bin/env python

import threading
import Queue
import time
import logging

# set logging.debug format
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] (%(threadName)s) %(message)s',)

# a worker thread for reading tasks from the 'taskqueue' Queue object, and
# adding messages to the 'logwriter' queue to be written to a logfile
class WorkerThread(threading.Thread):
	def __init__(self, inQueue, outQueue):
		threading.Thread.__init__(self)
		self.inQueue = inQueue
		self.outQueue = outQueue

	def run(self):
		while True:
			counter = self.inQueue.get()
			print "process %d" % counter
			#logging.debug('processing value %d' % counter)
			#time.sleep(2)
			self.outQueue.put("Bananas processed this cycle " + str(counter))
			print "done %d" % counter
			#logging.debug('value %d processed' % counter)
			self.inQueue.task_done()

# a worker thread for reading log entries from the 'logqueue' Queue object, and
# writing them to a logfile
class LoggingWorkerThread(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			nextLog2Write = self.queue.get()
			logging.debug(nextLog2Write)
			self.queue.task_done()

# main function - main application logic
def main():
	# instantiate queues to allow data to flow between thread in the application
	taskqueue = Queue.Queue()
	logqueue = Queue.Queue()

	# create logging thread and start it
	logwriter = LoggingWorkerThread(logqueue)
	logwriter.setName('LOGWRITER')
	logwriter.setDaemon(True)
	logwriter.start()

	# create worker thread for processing values (and start them)
	for i in range(3):
		worker = WorkerThread(taskqueue, logqueue)
		worker.setDaemon(True)
		worker.start()
		print "Worker %d created." % i

	# ===

	# add some integers to the 'taskqueue' Queue object
	for j in range(10):
		taskqueue.put(j)

	# "join" queue - by invoking this method we are comitting to waiting for all 
	# tasks on a queue to be completed

	taskqueue.join()

	# for some reason the main application won't exit at the moment, without adding
	# a timeout to this 'join'...

	logwriter.join()

if __name__ == "__main__":
	main()

