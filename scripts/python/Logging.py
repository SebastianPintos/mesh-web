import socket, time
print ()

UDP_IP = "0.0.0.0"

UDP_PORT = 5007


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
with open("data.log", "a") as myfile:
        myfile.write(time.strftime("%H:%M:%S - %d/%m/%Y")+" - SERVER STARTED   \n")
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    with open("data.log", "a") as myfile:
        myfile.write(time.strftime("%H:%M:%S - %d/%m/%Y")+" - "+data+"\n")
    print(time.strftime("%H:%M:%S - %d/%m/%Y")+" - "+data+"\n")
