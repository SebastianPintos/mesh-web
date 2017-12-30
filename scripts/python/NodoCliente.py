from socket import *
import time,traceback

UDP_PORT_Arduino = 8888
IP_NODO_MASTER= '10.10.5.5'
PUERTO_NODO_MASTER= 5005

def enviarUDP(IP,port,message):
    print("\n/////// Enviar UDP ///////\n")
    print("Creando Socket...")
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
    except:
        print("error")
        print("\n/////// FIN Enviar UDP ///////")
        return
    print("listo")
    print("Enviando Mensaje...")

    try:
        sock.sendto(message, (IP, port))
    except:
        print("error")
        print(traceback.format_exc())
        print("\n/////// FIN Enviar UDP ///////")
        return
    print("listo")
    print("\n/////// FIN Enviar UDP ///////")



def escucharMensajesArduino():
    print("Abriendo Socket...")

    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(("0.0.0.0", UDP_PORT_Arduino))
    except:
        print("error")
        print(traceback.format_exc())
        print("Reintentando...\n")
        time.sleep(3)
        escucharMensajesArduino()# Reintento Abrir socket
        return

    print("listo")

    while True:
        print("\n/////Escuchando Arduino/////\n")
        print("...")
        try:
            data,addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        except:
            print("error")
            escucharMensajesArduino()
            return
        print(" ok\n")
        print(data)
        print("\nEnviando a NodoMaster...")
        print("\n/////FIN Escuchando Arduino/////")
        enviarUDP(IP_NODO_MASTER,PUERTO_NODO_MASTER,data)

print("\n//////////NODO CLIENTE/////////\n")
escucharMensajesArduino()
