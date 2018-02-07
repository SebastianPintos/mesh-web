import socket, threading

UDP_IP = "0.0.0.0"
<<<<<<< Updated upstream
UDP_PORT = 5005
=======
UDP_PORT = 5007
>>>>>>> Stashed changes

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message:", data)
