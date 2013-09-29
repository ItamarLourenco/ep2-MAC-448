import sys
import socket

class ChatServer:
	def __init__(self, port):
		self.tcpConnections = {}
		self.udpConnections = {}
		self.socket = socket.socket ()
		self.port = int(port)

	def start(self, port):
		host = socket.gethostname() # Get local machine name
		print host
		port = self.port                 # Reserve a port for your service.
		self.socket.bind((host, port))        # Bind to the port

		print("Server is (or should be) runnning at " + host + ":" + port)

		self.socket.listen(5)                 # Now wait for client connection.
		while True:
		   c, addr = self.socket.accept()     # Establish connection with client.
		   print 'Got connection from', addr
		   c.send('Thank you for connecting')
		   c.close()                # Close the connection

def main():
	# tratar a entrada troll aqui
    server = ChatServer(sys.argv[1])
    server.start(server.port)


if  __name__ =='__main__':
    main()