#Yong Lee
#leey2@onid.oregonstate.edu
#cs344-400
#Homework 6
#Some codes taken from http://ilab.cs.byu.edu/python/socket/echoserver.html
#http://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php

import select
import socket
import sys
import os
import time
import signal


# broadcast chat messages to all connected clients
def broadcast (sock, message):
	for socket in CONNECTION_LIST:
		# send the message only to peer
		if socket != server and socket != sock :
			try :
				socket.send(message)
			except :
				# broken socket connection
				socket.close()
				# broken socket, remove it
				CONNECTION_LIST.remove(socket)
	
	
def handler1(signum, frame):
	print 'Process Interrupted.'
	sys.exit(0)
	
def handler2(signum, frame):
	print 'Connection Hung up.'
	sys.exit(0)
	
def handler3(signum, frame):
	print 'Process Quit.'
	sys.exit(0)
	
if __name__ == "__main__":
	signal.signal(signal.SIGINT, handler1)
	signal.signal(signal.SIGHUP, handler2)
	signal.signal(signal.SIGQUIT, handler3)


	HOST = ''
	CONNECTION_LIST = []
	PORT = 9879
	backlog = 5
	size = 1024

	server = None

	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server.bind((HOST, PORT))
		server.listen(backlog)
	except socket.error, (value,message):
		if server:
			server.close()
		print "Could not open socket: " + message
		sys.exit(1)

	CONNECTION_LIST.append(server)
		
	input = [server,sys.stdin] 
	running = 1 


	count = 0
	temp = ""
	flop = 0
	ulimit = 1
	llimit = 1
	callimit = 1
	pnumarray = []
	temporary = []
	info = []

	while running:
		inputready,outputready,exceptready = select.select(CONNECTION_LIST,[],[])

		for s in inputready:

			if s == server:
				# handle the server socket
				client, address = server.accept()
				CONNECTION_LIST.append(client)
				
			else:
				# handle all other sockets
				data = s.recv(size)
				
				if data:
					while (data[count] != ">"):
						if (data[count] != "<"):
							temp = temp + data[count]
						count = count + 1
				
				
					#check if data is flop and send limits
					if temp == "flop":
						count = count + 1
						temp = ""
						while (data[count] != "<"):
							temp = temp + data[count]
							count = count + 1

						flop = int(temp) + 1

						callimit = llimit
						
						#calculate limits
						while (callimit < flop):
							callimit = callimit + ulimit
							ulimit = ulimit + 1
													
						
						data = ""
						data = "<llimit>" + str(llimit) + "</llimit><ulimit>" + str(ulimit) + "</llimit>"
						
						llimit = ulimit + 1
						
						s.send(data)
						
						data = ''
						temp = ''
						count = 0
					
					
					#check if data contain perfect number and info
					if temp == "host":
						count = 0
						
						while data[count] != ">":
							count = count + 1
						count = count + 1
						
						#get hostname
						temp = ''
						while (data[count] != "<"):
							temp = temp + data[count]
							count = count + 1
							
						temporary.append(temp)
						
						while data[count] != ">":
							count = count + 1
						count = count + 1
						while data[count] != ">":
								count = count + 1
										
						count = count + 1
						
						#get process id
						temp = ''
						while (data[count] != "<"):
							temp = temp + data[count]
							count = count + 1
						
						temporary.append(temp)
						
						while data[count] != ">":
							count = count + 1
						count = count + 1
						while data[count] != ">":
							count = count + 1
										
						count = count + 1
							
						#get lower limit
						temp = ''
						while (data[count] != "<"):
							temp = temp + data[count]
							count = count + 1
						
						temporary.append(temp)
						
						while data[count] != ">":
							count = count + 1
						count = count + 1
						while data[count] != ">":
							count = count + 1
										
						count = count + 1
						
						#get upper limit
						temp = ''
						while (data[count] != "<"):
							temp = temp + data[count]
							count = count + 1
						
						temporary.append(temp)
						
						info.append(temporary);
						
						
						while data[count] != ">":
							count = count + 1
						count = count + 2
						
						temp = ''
						while (data[count] != ">"):
							temp = temp + data[count]
							count = count + 1
						
						#get perfect number if any
						if temp == "pnum":
							while temp == "pnum":
								temp = ''
								count = count + 1
								while (data[count] != "<"):
									temp = temp + data[count]
									count = count + 1
									
								pnumarray.append(temp)
								
								while data[count] != ">":
									count = count + 1
								count = count + 2
								
								temp = ''
								while (data[count] != ">"):
									temp = temp + data[count]
									count = count + 1
							
						
						temporary = []
						
						data = ''
						temp = ''
						count = 0
						
						data = "end"
						s.send(data)
						data = ''

					if temp == "report":
						data = ''
						
						count = 0
						while count < len(pnumarray):
							data = data + "<pnum>" + pnumarray[count] + "</pnum>"
							count = count + 1
							
						count = 0
						while count < len(info):
							data = data + "<host>" + info[count][0] + "</host>"
							data = data + "<processid>" + info[count][1] + "</processid>"
							data = data + "<lowerlimit>" + info[count][2] + "</lowerlimit>"
							data = data + "<upperlimit>" + info[count][3] + "</upperlimit>"
							count = count + 1
							
						data = data + "<end>"
						s.send(data)
						
						data = ''
						temp = ''
						count = 0
						
					if temp == "intr":
						broadcast (client, "kill")
						os.kill(os.getpid(), signal.SIGINT)
						
				else:
					s.close()
					CONNECTION_LIST.remove(s)
	server.close() 

