# Encrypted Messaging Service

This program is a python-based socket connection messaging service utilizing RSA encryption for end-to-end encryption of messages between a server and a client

To run the program, you need to create 5 text files:
- ip.txt
- pCLient.txt
- qClient.txt
- pServer.txt
- qServer.txt

the `ip.txt` file holds the ip or url of the host to bind to for the server

the other files hold a prime self that will be used to encrypt the messages

# TODO

- send the smaller sized integers over the socket using shrinkIntToSendOverSocket()
- properly send messages over the socket
- properly encode and decode
- maybe set up wireshark and intercept packets going to and from the server so we can find the messages


