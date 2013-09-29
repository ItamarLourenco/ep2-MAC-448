import sys
import socket

class ServerConnection:
	def __init__(self, host, port):
		self.socket = socket.socket()         # Create a socket object

		self.host = host
		self.port = port

		self.socket.connect((self.host, self.port))
		print self.socket.recv(1024)
		self.socket.close                     # Close the socket when done
		

class ChatClient:
	def __init__(self):
		pass

	def start(self):
		print("aqui ficaria uma lista de opcoes para o usuario")
		cmd = raw_input("Digite um comando e as opcoes correspondentes: ")
		while  cmd != "q" :
			params = cmd.split(" ")
			if params[0] == "c": #connect to server
				self.conn = ServerConnection(params[1], int(params[2]))
			cmd = raw_input("Digite um comando e as opcoes correspondentes: ")

def main():
    client = ChatClient()
    client.start()


if  __name__ =='__main__':
    main()