import socket
import ssl
import threading
import datetime
import random
import hashlib

KEYFILE = 'openssl/private.key'
CERTFILE = 'openssl/server.crt'

def shake_salt():
	alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	chars=[]
	for i in range(16):
		chars.append(random.choice(alphabet))
	return("".join(chars))


def handle_client(client_socket):
	
	client_socket.send(b"auth")
	request = client_socket.recv(2048)
	s = request.decode()
	#print(s)
	auth = request.decode()
	username, password = auth.split(",")
	flag = 0
	with open("users/credentials", "r") as f:
		lines = f.readlines()
		for i in lines:
			creds = i.split("\t")
			if(creds[0] == username):
				p_s = password+creds[2]
				h = hashlib.sha256(p_s.encode('utf-8')).hexdigest()
				if h == creds[1]:
					flag = 1
					client_socket.send(b"pass")
					break
				else:
					flag = 1
					client_socket.send(b"fail")
					break
	if flag == 0:
		with open("users/credentials", "a") as f:
			client_socket.send(b"reg")
			salt = shake_salt()
			p_s = password+salt
			h = hashlib.sha256(p_s.encode('utf-8')).hexdigest()
			f.write(username + "\t" + h + "\t" + salt + "\n")

	while True:
		request = client_socket.recv(2048)
		var = request.decode()

		if(var[:3] == "END"):
			print("[*] Ending a connection")
			break
		elif(var[:3] == "GET"):
			filepath = var[3:].strip(" ")
			filepath = 'groups/' + filepath
			try:
				with open(filepath, "rb") as f:
					client_socket.send(f.read())
			except:	
				client_socket.send(b"No group found")
		elif(var[:4] == "POST"):
			args = var[4:].split("\"")
			if(len(args)<2):
				client_socket.send(b"Input error")
				continue
			else:
				filepath = 'groups/' + args[0].strip(" ")
				t = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
				string = args[1]+"\t"+username+"\t"+t+"\n"
				with open(filepath, "a+") as f:
					f.write(string)
					s = "Added " + string + " to group" + args[0] 
					r = s.encode()
					client_socket.send(r)
		else:
			break
	
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