import socket

HOST = '127.0.0.1'    # The remote host
PORT = 5555                # Arbitrary non-privileged port
# Echo client program


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while(1):
    strw = 'G'+str(0)+' ' + 'Z' + str(3)
    s.sendall(strw.encode())
