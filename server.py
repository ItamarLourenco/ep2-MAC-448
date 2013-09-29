import sys
import socket

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
		self.socket.bind((host, port))        # Bind to the port

		print("Server is (or should be) runnning at " + host + ":" + str(port))

		self.socket.listen(self.maxConn)                 # Now wait for client connection.
		while True:
		   c, addr = self.socket.accept()     # Establish connection with client.
		   print 'Got connection from', addr
		   c.send("Ola , seja bem-vindo ao server da zuera sem fim")
		   connString = c.recv(4096)
		   connParams = connString.split(" ")
		   if connParams[0] == "tcp":
		   		self.tcpConnections[connParams[1]] = c
		   #c.close()                # Close the connection

#port maxConnections
def main():
	# tratar a entrada troll aqui
    server = ChatServer(int(sys.argv[1]), int(sys.argv[2])) 
    server.start()


if  __name__ =='__main__':
    main()