import socket, threading
import logging

UDP_IP = "0.0.0.0"

UDP_PORT = 5005


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

UDP_SERVER_PORT = 5005
UDP_SERVER_IP = "129.168.1.2"

logger = logging.getLogger("Error logger")
logger.setLevel(logging.INFO)

fh = logging.FileHandler('error.log')

logger.addHandler(fh)

try:
    sock_recv = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock_recv.bind((UDP_IP, UDP_PORT))

    sock_sender = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
except Exception as e:
    print("Entro bien a la excepcion")
    logger.info("Esta es la escepcion")

while True:
    data, addr = sock_recv.recvfrom(1024) # buffer size is 1024 bytes
    print("received message:", data)
    sock_sender.sendto(data, (UDP_SERVER_IP, UDP_SERVER_PORT))
