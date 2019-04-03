import socket

UDP_IP = "127.0.0.1"
UDP_PORT = [5000,5001,5002,5003]
MESSAGE = input().encode()

n_port = len(UDP_PORT)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
for i in range(n_port):
    sock.sendto(MESSAGE, (UDP_IP,UDP_PORT[i]))
    sock.settimeout(0.2)