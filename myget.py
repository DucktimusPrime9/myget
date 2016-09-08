#!/usr/bin/python
# Guadalupe Delgado & Blaise Cannon
# Lab 3 Re-do!

import sys
from urlparse import urlparse
from socket import *
import time
import re

# accepts arguments using sys.argv
# sys.argv = ['cscLab1.py','http;//www.centre.edu/index.html','F'] # used for testing

# args = []

# for arg in sys.argv:
#   args.append(arg)

URL = sys.argv[1] # arg 1
filename = sys.argv[2] # arg 2

#print URL
#print filename

# Parses the URL
ParseResult = urlparse(URL)
#print ParseResult

# Sets port value
if ParseResult.port is None: # if it does not have a port
		port = 80 # set port to 80
		print "Port set to: ",port
else:
	# else use the port given
		print "Port set to: ",ParseResult.port

#  code from the book to establish  conncetion
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((ParseResult.hostname, port))
request = 'GET ' + ParseResult.path + ' HTTP/1.1\r\nHost: ' + ParseResult.hostname +'\r\n\r\n'
clientSocket.send(request)

# It gets content and stores it in a variable where it iterates to find the double
# carriage return
getcont = "" # this is where I save the content
while getcont.find('\r\n\r\n') == -1: # you look for the double carriage return
	getcont += clientSocket.recv(1)# asks the socket for a byte

getHead = getcont[0:getcont.find("\r\n\r\n")] # find all of the head info
headerlist = getHead.split('\r\n') # this splits our header into multiple lines so that we can manipulate content length much easier

# this actually finds the line with content length and returns it
for line in headerlist:
	if "Content-Length:" in line:
		contentLength = line

contentLength = contentLength[16:] # look for content length, set to var when found
getcont = getcont[getcont.find("\r\n\r\n")+4:] # checks to make sure that no information is left

datacount = int(len(getcont))
contentLength = int(contentLength)

print "Request sent."
while datacount <= contentLength:
		newcont = clientSocket.recv(2048)
		datacount = datacount + len(newcont)
		getcont = getcont + newcont # asks the socket for 2048 bytes
		if datacount == contentLength:
			break
print "Request completed."

clientSocket.close()
errorCode = getHead[getHead.find("HTTP/1.1 ") + 9:12]

# getHead is the header until the return
# we find the HTTP/1.1 header
if len(sys.argv) < 2: # checks to see how many arguments i have
		print "Not enough arguments."
else:
		if errorCode == '200':
				output = open(filename, "w")
				output.write(getcont)
				output.close()
		else:
				output = open(filename, "w")
				#output.write('')
				output.close()