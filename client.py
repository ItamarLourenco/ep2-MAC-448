#!/usr/bin/env python

import sys
import socket
import thread
import time
import sys

global clientConnection
global connectWithServer

class ClientConnection:
	def __init__(self, mode):
		self.clientSocket = socket.socket()         # Create a socket object
		self.clientSocket.bind(('', 0))
		self.port = self.clientSocket.getsockname()[1]
		print str(self.port)
		self.peer = ""
		self.sSocket = None
		self.rSocket = None

	def send(self):
		msg = "  "
		msgS = [msg]
		while msgS[0] != "<close>":
			msg = raw_input("\nYou >>")
			msgS = msg.split(" ")
			self.sSocket.send(msg)

	def recieve(self):
		msg = "  "
		msgS = [msg]
		while msgS[0] != "<close>":
			msg = self.rSocket.recv(4096)
			msgS = msg.split(" ")
			print ("\n\n"+self.peer+" >> " + msg + "\nYou >>"),
			
	def connect(self, peer, host, port):
		self.peer = peer
		print "vou me conectar a " + str(host) + " " + port
		self.sSocket = socket.socket()
		print "criei socket de envio"
		self.rSocket = socket.socket()
		print "criei socket de resposta"
		self.rSocket.connect((host, int(port)))
		print "socket de resposta pronto"
		self.sSocket.connect((host, int(port)))
		print "socket de envio pronto"
		self.rSocket.settimeout(60)
		try:
			msg = self.rSocket.recv(4096)
		except socket.timeout:
			self.sSocket.close()
			self.rSocket.close()
			print ("\nconexao falhou\n")
			connectWithServer = True
			return
		if msg == "<accept>":
	   		thread.start_new_thread(self.recieve, ())
	   		thread.start_new_thread(self.send, ())			
			print ("\nconexao bem sucedida\n")

	def listen(self, nickname):
		# print "to escutando na port " + str(self.port)
		self.clientSocket.listen(2)
		while True:
			if (self.peer == ""):
				print "achei socket de resposta"
				self.sSocket, addr = self.clientSocket.accept()
				print "esperando socket de resposta"
				self.rSocket, addr = self.clientSocket.accept()
				print "achei socket de envio"
				self.peer = nickname
				print "recebi os sockets de "+nickname
				msg = "<accept>"
				self.sSocket.send(msg)
		   		thread.start_new_thread(self.recieve, ())
		   		thread.start_new_thread(self.send, ())			
			else:
				break

class ServerConnection:
	def __init__(self, host, port, mode, nickname):
		self.serverSocket = socket.socket()         # Create a socket object
		self.host = host
		self.port = port
		self.mode = mode
		self.nickname = nickname
		self.serverSocket.connect((self.host, self.port))
		print self.serverSocket.recv(4096)
		self.clientConnection = ClientConnection(mode)
		self.serverSocket.send(mode + " " + nickname + " "+str(self.clientConnection.port))
		self.connectWithServer = True
		self.peerToPeerListener = None
		thread.start_new_thread(self.listenServer, ())

	def listenServer(self):
		shouldPrint = True
		while True:
			# print "\nclientInternals: esperando resposta do servidor\n"
			recString = self.serverSocket.recv(4096)
			# print "Server mandou " + recString
			if recString == "?Alive?":
				self.serverSocket.send("(Y)")
				shouldPrint = False
			
			recs = recString.split(" ")
			if recs[0] == "<connect>":
				# print recString
				self.connectWithServer = False
				print("\n"+recs[1] + " quer se conectar com vc. Aceitar?(s/n)")
				action = raw_input("")
				while (not action == "Belesma"):
					print action
					if(action == "s"):
						self.clientConnection.connect(recs[1], recs[2], recs[3])
						action == "Belesma"
						break
					if(action == "n"):
						self.serverSocket.send("<release> "+recs[1])
						self.connectWithServer = True
						action == "Belesma"
						break
					else:
						print(recs[1] + "quer se conectar com vc. Aceitar?(s/n)")
						action = raw_input("")
				shouldPrint = False

			if recString == "<release>":
				self.connectWithServer = True
				if not self.peerToPeerListener == None:
					self.peerToPeerListener._Thread__stop()
				shouldPrint = False

			if shouldPrint :
				print recString

			shouldPrint = True

class ServerTCPConnection(ServerConnection):
	def __init__(self, host, port, mode, nickname):
		ServerConnection.__init__(self, host, port, mode, nickname)
	
	def listen(self):
		print("Para uma lista de comandos validos digite cmd")
		cmd = raw_input("Digite um comando e as opcoes correspondentes: ")
		# global connectWithServer = True
		tmp = []
		while  cmd != "q" and cmd != "quit" :
			if (self.connectWithServer):
				tmp = cmd.split(" ")
				if tmp[0] == "connect":
					print "tentando se conectar com "+tmp[1]
					self.serverSocket.send(cmd)
					self.connectWithServer = False
					self.peerToPeerListener = self.clientConnection.listen(tmp[1])
				else:
					self.serverSocket.send(cmd)
					time.sleep(0.5)
					cmd = raw_input("Digite um comando e as opcoes correspondentes: ")

		self.serverSocket.shutdown(0)
		self.serverSocket.close()


class ServerUDPConnection(ServerConnection):
	def __init__(self):
		ServerConnection.__init__(self)

class ChatClient:
	def __init__(self):
		pass

	def ComunicateWithClient (self, host, port, mode):
		pass

	def start(self):
		if sys.argv[3] == "tcp":
			self.conn = ServerTCPConnection(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])
		elif sys.argv[3] == "udp":
			self.conn = ServerUDPConnection(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])

		self.conn.listen()

# server port mode nickname
def main():
    client = ChatClient()
    client.start()


if  __name__ =='__main__':
    main()