import socket
import ssl

HOSTNAME = "www.google.com"

context = ssl.create_default_context()
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname=True
context.load_verify_locations("/etc/ssl/certs/ca-certificates.crt")
conn = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=HOSTNAME)
conn.connect((HOSTNAME,443))
cert = conn.getpeercert()

print(cert)