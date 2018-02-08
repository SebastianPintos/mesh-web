import socket, time , sys

logName="log.txt"
def log(message):
    timeStamp=time.strftime("%H:%M:%S - %d/%m/%Y")+" - "
    with open(logName, "a") as myfile:
        myfile.write(timeStamp+message+"\n")
    print(timeStamp+message+"\n")
UDP_IP = "0.0.0.0"
UDP_PORT = 5009
if(len(sys.argv)==2):
	UDP_PORT = int(sys.argv[1])
log("Logging initializing...\n")
log("Binding to "+str(UDP_IP)+":"+str(UDP_PORT))
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

log("SERVER STARTED...");

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    log(data)

