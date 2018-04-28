Nicholas Harras


CS419 -- Assignment 6: OpenSSL Message Board Project
====================================================

This is a server/client program written in Python3. You run it simply by running

$python server.py

And then by running...

$python client.py

All interaction is handled on the client end. Clients must first sign in. 
Default credentials are as follows... username: nick, password: password and 
username: dan, password: rocky1. However, any new account is added to the 
credentials file.

There is a bug here which is the consequence of poor planning. If you enter 
the wrong password for an existing user, the program does not accept the user's
correct password. This is a looping error caused on the server side (it doesn't
expect credentials to be failed).

When users are registered, a random salt is generated and associated with their
account in the "credentials" file (in the "users" directory). Each entry in the
credentials file consists of a username, followed by their salted password hash 
in sha256, and their salt. The salts are used to verify the hashes of existing
users.

The once the client is logged in, he/she has the ability to POST (append) any 
content to a file. This string is taken, concatenated with the username, and the
current timestamp. Each newline represents a new post. Clients may create new 
group files at whim with this command. All group files are stored in the "groups"
directory.

A client may also GET, which prints the contents of an existing group file. When
GET tries to access a non-existant file, it simply prompts the user again.

A client may finally END their session, which simply closes their socket.

The server client is multi-threaded via the "threading" module.

Lastly, all packets sent over the network are wrapped as SSL sockets and are 
thusly secure from inspection. The self-signed certificate associated with the 
server is verified by the client when he/she establishes the connection. 

I think that is everything. All group files are dummy placeholders. Any new 
groups and new users can be created very easily.

Best!
-Nick