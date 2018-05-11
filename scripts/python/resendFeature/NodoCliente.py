from socket import *
import time,traceback
import json
from informationStamper import *
from routeToHost import *
from UdpConnection import *
from FileManagement import *
from PackagesResender import *

IP_LOCAL_NODE = '10.10.5.1'
UDP_PORT_Arduino = 8888
IP_NODO_MASTER= '192.168.1.35'
PUERTO_NODO_MASTER= 5005
BUFFER_FILE_NAME = "bufferFile.txt" #TODO Podría ser recibido como parámetro esto

need_to_send_buffer = False

list_stampers = [TimestampStamper(), IpStamper()]
json_stamper = InformationStamper(list_stampers)

route_to_host = RouteEntablishedDetector(IP_NODO_MASTER)

udpListener = UdpListener("0.0.0.0", UDP_PORT_Arduino) #TODO armar una clase para poner toda esta bola
udpSender = UdpSender(IP_NODO_MASTER, PUERTO_NODO_MASTER)

fileWritter = FileWritter(BUFFER_FILE_NAME)

def enviarUDP(message):

    if route_to_host.is_entablished_route():
        global need_to_send_buffer
        if (need_to_send_buffer): #Que pasa si se corta la conexión justo cuando estoy reenviando -> UDP va a seguir enviando
            #Aquí utilizando UDP hay una potencial pérdida de información
            fileLineReader = FileLineReader(BUFFER_FILE_NAME)
            fileDeletor = FileDeletor(BUFFER_FILE_NAME)
            bufferResender = PackageResender(fileLineReader, udpSender)
            bufferResender.resend_all_buffered_packets()
            need_to_send_buffer = False
            fileDeletor.delete()

        udpSender.send(message)
        print(message)
    else:
        fileWritter.write(message)
        need_to_send_buffer = True

def escucharMensajesArduino():

    while True:
        data,addr = udpListener.listen()  # buffer size is 1024 bytes
        # json decode
        json_data = json.loads(data.decode('utf-8'))
        # Ponerla la ip y el timestamp
        json_stamper.stamp_info(json_data)
        # Volver a codificar
        to_send = json.dumps(json_data)
        print("\nEnviando a NodoMaster...")
        enviarUDP(to_send)

print("\n//////////NODO CLIENTE/////////\n")
escucharMensajesArduino()
