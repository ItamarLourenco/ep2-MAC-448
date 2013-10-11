#!/usr/bin/env python


import sys
import socket
import thread

class Client:
	def __init__(self, conn, nickname):
		self.conn = conn
		self.nickname = nickname


class ChatServer:
	def __init__(self, port, maxConn):
		self.tcpConnections = {}
		self.udpConnections = {}
		self.socket = socket.socket()
		self.port = port
		self.maxConn = maxConn

	def start(self):
		host = socket.gethostname() # Get local machine name
		port = self.port                 # Reserve a port for your service.
		self.socket.bind(('', port))        # Bind to the port

		print("Server is (or should be) runnning at " + host + ":" + str(port))

		self.socket.listen(self.maxConn)                 # Now wait for client connection.
		while True:
		   c, addr = self.socket.accept()     # Establish connection with client.
		   c.send("Ola , seja bem-vindo ao server da zuera sem fim")
		   connString = c.recv(4096)
		   connParams = connString.split(" ")
		   print 'Got connection from', connParams[1], addr
		   if connParams[0] == "tcp":
		   	#socket de conexao com o cliente, endereco (ip, port), porta para P2P, cliente conectado com ele P2P
		   		self.tcpConnections[connParams[1]] = c, addr, connParams[2], "" 
		   		thread.start_new_thread(self.handleTCPConnection, (connParams[1], ))

	def help (self, cmd, conn):
		if len(cmd) > 0:
			if cmd == "list":
				conn.send("\nLista usuarios conectados ao servidor\nUso: list")
			if cmd == "connect":
				conn.send("\nSe conecta ao usuario passado como parametro\nUso: connect <usuario>")
			if cmd == "help":
				conn.send("\nExibe informacoes e instrucao de uso sobre comando passado por parametro\nUso: help <comando>")
			if cmd == "quit":
				conn.send("\nTermina a execucao do programa cliente\nUso: quit")
			if cmd == "cmd":
				conn.send("\nLista comandos disponiveis\nUso: cmd")
		else:
			conn.send("\nComando desconhecido. Digite cmd para obter lista de comandos validos\n")

	validCommands = [
		["list",
		"connect",
		"cmd", 
		"help",
		"quit"],
		["_close_",
		"_conect_",
		"_list_"
		]
	]


	def ParseCMD (self, cmd, nickname):
		if cmd[0] == "list":
			self.tcpConnections[nickname][0].send("\nUsuarios conectados:\n")
			for a in self.tcpConnections.keys():
				self.tcpConnections[nickname][0].send(str(a) + "\n")
			return

		if cmd[0] == "connect":
			if len(cmd) == 2:
				self.tcpConnections[nickname][0].send("Conectando a "+cmd[1] + "\n")
				print "Conectando "+ nickname +" a "+cmd[1]
				if cmd[1] == nickname:
					self.tcpConnections[nickname][0].send("nao eh possivel se conectar a si mesmo")
					print "nao eh possivel se conectar a si mesmo"
				else:
					if cmd[1] in self.tcpConnections.keys() and self.tcpConnections[cmd[1]][3] == "":
						rec = nickname+ " " + str(str(self.tcpConnections[cmd[1]][1][0]))+ " " + str(self.tcpConnections[nickname][2])
						self.tcpConnections[cmd[1]][0].send("<connect> " + rec)
						# print nickname+ " " + str(str(self.tcpConnections[cmd[1]][1][0]))+ " " + str(self.tcpConnections[nickname][2])
						self.tcpConnections[nickname][3] == cmd[1]
					else:
						print "releaseando"
						self.tcpConnections[nickname][0].send("<release>")
			else:
				self.help(cmd[0], self.tcpConnections[nickname][0])
			return

		if cmd[0] == "<connected>":
			if cmd[1] in self.tcpConnections.keys():
				self.tcpConnections[cmd[1]][0].send("<release>")
				self.tcpConnections[nickname][3] == cmd[1]

		if cmd[0] == "<release>":
			if cmd[1] in self.tcpConnections.keys():
				self.tcpConnections[cmd[1]][0].send("<release>")

		if cmd[0] == "help":
			if not len(cmd) == 2:
				self.help(cmd[0], self.tcpConnections[nickname][0])
			else:
				self.help(cmd[1], self.tcpConnections[nickname][0])
			return

		if cmd[0] == "cmd":
			self.tcpConnections[nickname][0].send("\n")
			if self.tcpConnections[nickname][3] == "":
				cmds = 0
			else:
				cmds = 1
			for a in self.validCommands[cmds]:
				self.tcpConnections[nickname][0].send(a + ":")
				self.help(a, self.tcpConnections[nickname][0])
				self.tcpConnections[nickname][0].send("\n\n")
			return


		if len(cmd[0]) > 0:
			self.tcpConnections[nickname][0].send("\nComando desconhecido. Digite cmd para obter lista de comandos validos\n")

	def TCPConnectionIsActive(self, nickname):
		self.tcpConnections[nickname][0].send("?Alive?")
		try:
			self.tcpConnections[nickname][0].settimeout(10)
			alive = self.tcpConnections[nickname][0].recv(4096)
		except socket.timeout:
			# print "\npeguei exception de timeout no socket teimoso\n"
			return False

		if (alive == "(Y)"):
			return True
		return False

	def handleTCPConnection(self, nickname):

		while True:

			try:
				self.tcpConnections[nickname][0].settimeout(60)
				print "esperando resposta de " + nickname
				recString = self.tcpConnections[nickname][0].recv(4096)
				print "recebi resposta de " + nickname
			except socket.timeout:
				# print "\npeguei exception de timeout no socket principal\n"
				if not self.TCPConnectionIsActive(nickname) :
					print nickname + " connection lost"
					break
				else:
					recString = ""
			
			if(recString == ""):
				if not self.TCPConnectionIsActive(nickname) :
					print nickname + " connection lost"
					break 
			else:
				print nickname + " - " + recString	
			
			cmd = recString.split(" ")

			self.ParseCMD(cmd, nickname)

			cmd = ""

		self.tcpConnections[nickname][0].close()
		del(self.tcpConnections[nickname])

	def handleUDPConnection(self, nickname):
		pass

#port maxConnections
def main():
	if len(sys.argv) < 3 or len(sys.argv) > 3:
		print "Uso: ./server <porta> <No_conexoes>"
		return
	server = ChatServer(int(sys.argv[1]), int(sys.argv[2]))
	server.start()


if  __name__ =='__main__':
    main()