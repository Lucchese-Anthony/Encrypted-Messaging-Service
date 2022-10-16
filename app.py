import socket           

# SETUP SOCKET SERVER
s = socket.socket()         # Create a socket object
port = 8080                 # Reserve a port for your service.
local_hostname = socket.gethostname()
ip = socket.gethostbyname("appname.herokuapp.com")
print(ip)
#ip = socket.gethostbyname(local_hostname)
#print(ip)
s.bind((ip, port))        # Bind to the port
print ('starting up on %s port %s' % (ip, port))