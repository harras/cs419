import socket
import ssl
import threading

KEYFILE = 'openssl/private.key'
CERTFILE = 'openssl/server.crt'


def handle_client(client_socket):
	request = client_socket.recv(1024)
	request_s = request.decode()
	print ("[*] Recieved: %s" %request_s)
	
	request_s = "".join(reversed(request_s))
	request = str.encode(request_s)

	# send back a packet
	client_socket.send(request)
	
	client_socket.close()

def server(address):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(address)
	s.listen(5)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	ssl_sock = ssl.wrap_socket(s, keyfile=KEYFILE, certfile=CERTFILE, server_side=True)

	print ("[*] Listening on {0}".format(address))

	while True:
		client,addr = ssl_sock.accept()
		print ("[*] Accepted connection from: %s:%d" %(addr[0], addr[1]))
		client_handler = threading.Thread(target=handle_client,args=(client,))
		client_handler.start()

server((socket.gethostbyname('localhost'), 5005))