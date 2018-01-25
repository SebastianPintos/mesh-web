import subprocess, socket, json, time, threading, paramiko
from mapView.models import Node, Location

def json_to_object(shellOutput):
	if isinstance(shellOutput, dict):
		n = {}
		for item in shellOutput:
			if isinstance(shellOutput[item], dict):
				n[item] = json_to_object(shellOutput[item])
			elif isinstance(shellOutput[item], (list, tuple)):
				n[item] = [json_to_object(elem) for elem in shellOutput[item]]
			else:
				n[item] = shellOutput[item]
		return type('obj_from_dict', (object,), n)
	elif isinstance(shellOutput, (list, tuple,)):
		l = []
		for item in shellOutput:
			l.append(shellOutput(item))
		return l
	else:
		return shellOutput

def retrieve_info():

	MASTER_NODE_IP = '129.168.1.1'
	MASTER_NODE_PORT='22'
	output=""

	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	#try:
	print ("Yes, im here")
	client.connect(MASTER_NODE_IP, MASTER_NODE_PORT, username='root', password='root', timeout=10)

	# except socket.timeout as TimeOut:
	# 	print("Trying again in a few seconds")
	# 	time.sleep(5)
	# 	retrieve_info()

	stdin, stdout, stderr = client.exec_command("echo \"/netjsoninfo GRAPH\" | nc 127.0.0.1 9001")# a properties

	print (stdout)
	for line in stdout:
	    output=output+line
	if output!="":
	    print ("")
	else:
	    print ("No funciona, lanzar excepción")

	client.close()

	return output

def get_active_ips(olsrObject):
	active_ips = []
	for item in olsrObject.collection:
		if item.topology_id == 'ipv4_0':
			for node in item.nodes:
				if node.properties.type == 'local' or node.properties.type == 'node':
					active_ips.append(node.properties.router_addr)

	print("These are the active ips: ", active_ips)
	return active_ips

def save_changes(active_ips):
	#Los nodos que pertencen a la tabla de ruteo se guardan como disponibles
	nodes = Node.objects.all()
	#Si un nodo no está en la tabla de ruteo es porqu está apagado

	for node in nodes:
		if (node.node_ip not in active_ips):
			node.node_states = 'ROJO'
		if (node.node_ip in active_ips and node.node_states == 'ROJO'):
			node.node_states = 'AMARILLO'

	#Esto no debería ir acá
	for node in nodes:
		print (node.node_ip, " | ", node.node_states)
		node.save()

def main(): #debería ser main
	while 1:
		raw_data = retrieve_info()
		node_info = json_to_object(json.loads(raw_data))

		save_changes(get_active_ips(node_info))
		#guardar cambios
		print ("Se guardó")
		time.sleep(15)


def retrieve_info_daemon():
	d = threading.Thread(target=main, name='retrieve')
	d.setDaemon(True)
	d.start()
