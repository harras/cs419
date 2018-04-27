import ssl
import socket

target_host = "127.0.0.1"
target_port = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssl_sock = ssl.wrap_socket(s,cert_reqs=ssl.CERT_REQUIRED,ca_certs='openssl/server.crt')
ssl_sock.connect((target_host, target_port))
cert = ssl_sock.getpeercert()

while True:
	var = str(input(">"))
	if var[:3] == "END":
		ssl_sock.write(var.encode())
		break
	elif var[:3] == "GET":
		file = var[3:].strip(" ")
		if file == "":
			print("GET must take a group name as an argument")
			print("\"GET <group name>\"")
			continue
		else:
			ssl_sock.write(var.encode())
	elif var[:4] == "POST":
		args = var[4:].split("\"")
		if len(args)<2:
			print("POST must take a group name and a string as an argument")
			print("\"POST <group name> \"<string>\"\"")
			continue
		else:
			ssl_sock.write(var.encode())
	elif var[:4].lower() == "help":
		print("Client operations:")
		print("GET <group name>")
		print("POST <group name> \"<string>\"")
		print("END")
	else:
		continue

	response = ssl_sock.recv(4096)
	print(response.decode())



ssl_sock.close()