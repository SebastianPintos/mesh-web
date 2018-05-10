from socket import *

class UdpSender:
    def __init__(self, to_send_ip, to_send_port):
        self.ip = to_send_ip
        self.port = to_send_port

        try:
            self.sock = socket(AF_INET, SOCK_DGRAM)
        except OSError as error:
            print(error)
            raise

    def send(self, message): #TODO debe lanzar
        self.sock.sendto(message.encode('utf-8'), (self.ip, self.port))

class UdpListener: #TODO Debe lanzar excepcion

    def __init__(self, binding_ip, binding_port):
        self.ip = binding_ip
        self.port = binding_port
        self.bufferSize = 1024

        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind((binding_ip, binding_port))


    def listen(self): #Listen queda lockeado
        return self.sock.recvfrom(self.bufferSize)
