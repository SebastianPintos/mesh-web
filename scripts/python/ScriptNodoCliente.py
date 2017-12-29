import socket
UDP_PORTArduino = 8888
TCP_IP = '10.10.5.5'
TCP_PORT = 5005
BUFFER_SIZE = 1024

def enviarAMaster(mensaje):

    MESSAGE = mensaje
    print("Iniciando Socket...")    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    s.close()

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    enviarAMaster(data)
    print ("received message:", data)
