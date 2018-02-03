from socket import *
import time,traceback
import json
import datetime

IP_LOCAL_NODE = '10.10.5.1'
UDP_PORT_Arduino = 8888
IP_NODO_MASTER= '10.10.5.5'
PUERTO_NODO_MASTER= 5005

def add_data(json_object):
    json_object['ip'] = get_mesh_ip()
    json_object['timestamp'] = get_timestamp()

def get_timestamp():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).isoformat()

def get_mesh_ip():
    return IP_LOCAL_NODE

def enviarUDP(IP,port,message):

    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.sendto(message, (IP, port))
    except:
        print("error")
        print(traceback.format_exc())
        return


def escucharMensajesArduino():
    print("Abriendo Socket...")

    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(("0.0.0.0", UDP_PORT_Arduino))#Sacar a archivo properties o como variable global
    except:
        print("error")
        print(traceback.format_exc())
        print("Reintentando...\n")
        time.sleep(5)
        escucharMensajesArduino()# Reintento Abrir socket
        return

    print("listo")

    while True:
        print("\n/////Escuchando Arduino/////\n")
        try:
            data,addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        except:
            print("error")
            escucharMensajesArduino()
            return
        # json decode
        json_data = json.loads(data.decode('utf-8'))
        # Ponerla la ip y el timestamp
        add_data(json_data)
        # Volver a codificar
        to_send = json.dumps(json_data)
        print(to_send)
        print("\nEnviando a NodoMaster...")
        print("\n/////FIN Escuchando Arduino/////")
        enviarUDP(IP_NODO_MASTER,PUERTO_NODO_MASTER,to_send)

print("\n//////////NODO CLIENTE/////////\n")
escucharMensajesArduino()
