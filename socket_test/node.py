import socket

UDP_IP = "127.0.0.1"
UDP_PORT = [5000,5001,5002,5003]
sock_list = []
n_port = len(UDP_PORT)

for i in range(n_port):
    sock_list.append(socket.socket(socket.AF_INET,socket.SOCK_DGRAM))

for i in range(n_port):
     sock_list[i].bind((UDP_IP,UDP_PORT[i]))

count = 0
interrupter = False
while count < 2:
    for i in range(n_port): 
        data, addr = sock_list[i].recvfrom(1024)
        if data != None:
            print("Now Connect Port Is ",UDP_PORT[i]) # UDP 포트가 몇번이 들어왔는지
    print("Received message : ", data.decode(), "Address :", addr[0],addr[1])
    data = None; addr = None; interrupter = False
    count += 1

