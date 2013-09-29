import sys
import socket
import thread

class ClientConnection:
	def __init__(self, host, port, mode):
		self.socket = socket.socket()         # Create a socket object
		self.host = host
		self.port = port
		self.mode = mode
		self.socket.connect((self.host, self.port))
		print self.socket.recv(4096)

	def send(self, message):
		pass

	def start(self):
		pass


class ServerConnection:
	def __init__(self, host, port, mode, nickname):
		self.socket = socket.socket()         # Create a socket object
		self.host = host
		self.port = port
		self.mode = mode
		self.nickname = nickname
		self.socket.connect((self.host, self.port))
		print self.socket.recv(4096)
		self.socket.send(mode + " " + nickname)
		thread.start_new_thread(self.listenServer, (0,))

	def listenServer(self, dummy):
		while True:
			recString = self.socket.recv(4096)
			print recString
		
class ServerTCPConnection(ServerConnection):
	def __init__(self, host, port, mode, nickname):
		ServerConnection.__init__(self, host, port, mode, nickname)
	
	def listen(self):
		print("aqui ficaria uma lista de opcoes para o usuario")
		cmd = raw_input("Digite um comando e as opcoes correspondentes: ")
		while  cmd != "q" :
			#params = cmd.split(" ")
			#if params[0] == "list": #connect to server
			self.socket.send(cmd)
			cmd = raw_input("Digite um comando e as opcoes correspondentes: ")
		self.socket.close()


class ServerUDPConnection(ServerConnection):
	def __init__(self):
		ServerConnection.__init__(self)

class ChatClient:
	def __init__(self):
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