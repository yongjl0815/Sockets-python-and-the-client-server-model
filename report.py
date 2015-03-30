#Yong Lee
#leey2@onid.oregonstate.edu
#cs344-400
#Homework 6
#Some codes taken from http://ilab.cs.byu.edu/python/socket/echoserver.html

import getopt
import socket
import sys
import os
import time
import signal



def handler1(signum, frame):
	print 'Process Interrupted.'
	sys.exit(0)
	
def handler2(signum, frame):
	print 'Connection Hung up.'
	sys.exit(0)
	
def handler3(signum, frame):
	print 'Process Quit.'
	sys.exit(0)

signal.signal(signal.SIGINT, handler1)
signal.signal(signal.SIGHUP, handler2)
signal.signal(signal.SIGQUIT, handler3)


HOST = sys.argv[1]
PORT = 9879
size = 1024

s = None

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
except socket.error, (value,message):
    if s:
        s.close()
    print "Could not open socket: " + message
    sys.exit(1)
	
s.send('<report></report>')

#try:
data = s.recv(size)
#except KeyboardInterrupt:


check = 0;

try:
	opts, args = getopt.getopt(sys.argv[2:], "k")
except getopt.GetoptError, err:
	print str(err)

for o, a in opts:
	if o == '-k':
		check = 1;
	else:
		print "nothing happened"

		
temp = ""
temp1 = ""
count  = 1

if data:
	while (data[count] != ">"):
		temp = temp + data[count]
		count = count + 1
	
	#print perfect number
	if temp == "pnum":
		print "Perfecr Number:"
		
		while temp == "pnum":
			temp = ''
			count = count + 1
			while (data[count] != "<"):
				temp = temp + data[count]
				count = count + 1
								
			#pnumarray.append(temp)
			print temp
			
			while data[count] != ">":
				count = count + 1
			count = count + 2
			
			temp = ''
			while (data[count] != ">"):
				temp = temp + data[count]
				count = count + 1
							
	#print host, process id, lower limit, upper limit
	print "\nProcesses:"
	print "Host :                           PID    Tested Range"
	while temp != "end":
		temp = ''
		count = count + 1
		while (data[count] != "<"):
			temp = temp + data[count]
			count = count + 1
			
		temp1 = temp1 + temp + "   "
			
		while data[count] != ">":
			count = count + 1
		count = count + 2
			
		temp = ''
		while (data[count] != ">"):
			temp = temp + data[count]
			count = count + 1
			
		if temp == "upperlimit":
			temp1 = temp1 + "-   "
			
		if temp == "host" or temp == "end":
			print temp1
			temp1 = ""
			
if check == 0:
	s.send('<done></done>')
elif check == 1:
	s.send('<intr></intr>')
	
s.close()
