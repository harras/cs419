import socket
import ssl
import threading

bind_ip= "127.0.0.1"
bind_port = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip, bind_port)

def handle_client(client_socket):

	request = client_socket.recv(1024)
	
	print "[*] Recieved: %s" %request
	
	request = ''.join(reversed(request))

	# send back a packet
	client_socket.send(request)
	
	client_socket.close()

while True:

	client,addr = server.accept()

	print "[*] Accepted connection from: %s:%d" %(addr[0], addr[1])

	client_handler = threading.Thread(target=handle_client,args=(client,))
	client_handler.start()