import socket, threading, json
from mapView.models import UdpPackage
from mapView.light_changes_detector import LightChangesAnalizer
from mapView.log_rotate import UdpPackageLogger


class UdpPackageParser:
    # recibo los datos crudos y luego los parseo a json
    def __init__(self):
        pass

    def parse_raw_data(self, raw_data):
        jsonpkg = json.loads(raw_data)

        # Buscar una mejor solución
        type = jsonpkg['type']
        del jsonpkg['type']
        ip = jsonpkg['ip']
        del jsonpkg['ip']
        timestamp = jsonpkg['timestamp']
        del jsonpkg['timestamp']

        return UdpPackage(type, ip, timestamp, jsonpkg)


class UdpListener:
    BUFFER_SIZE = 1024
    parser = UdpPackageParser()

    def __init__(self, udp_ip, udp_port):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.analyzer = LightChangesAnalizer() # Esto no es responsabilidad de UD
        self.logger = UdpPackageLogger()

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.bind((self.udp_ip, self.udp_port))

        while 1:
            data, addr = sock.recvfrom(self.BUFFER_SIZE)  # buffer size is 1024 bytes

            udp_package = self.parser.parse_raw_data(data.decode())
            print(udp_package.type)
            self.analyzer.analyze_data(udp_package) #analizo el paquete
            self.logger.log_pkg(udp_package)#Logeo paquete


# Además, inicializar un deamon
def udp_handler_daemon():
    udpListener = UdpListener("0.0.0.0", 5005)
    d = threading.Thread(target=udpListener.listen, name='listener')
    d.setDaemon(True)
    d.start()
