import socket, threading, json
from mapView.light_changes_detecter import LightChangesAnalizer

class LightStateParser:
    #recibo los datos crudos y luego los parseo a json
    def parse_raw_data(self, raw_data):
        print("received message:", raw_data)
        toRet = json.loads(raw_data)
        print(toRet)
        return toRet


class UdpListener:
    BUFFER_SIZE = 1024
    parser = LightStateParser()

    def __init__(self, udp_ip, udp_port):
        self.udp_ip = udp_ip
        self.udp_port = udp_port

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.bind((self.udp_ip, self.udp_port))

        while 1:
            data, addr = sock.recvfrom(self.BUFFER_SIZE) # buffer size is 1024 bytes
            self.parser.parse_raw_data(data.decode())
            #Acá poner el parser

#Además, inicializar un deamon
def udp_handler_daemon():
    udpListener = UdpListener("0.0.0.0", 5005)
    d = threading.Thread(target = udpListener.listen , name ='listener')
    d.setDaemon(True)
    d.start()
