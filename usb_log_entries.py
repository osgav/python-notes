#!/usr/bin/env python

import os

try:
	logfile = open("/var/log/dmesg", "r")
except IOError as e:
	print "Permissions error: " + str(e)
except Exception as e:
	print "No idea: " + str(e)
else:
	logfilecontents = logfile.readlines()
	usbitems = [s for s in logfilecontents if "usb" in s]
	for entry in usbitems:
		print entry.strip()

