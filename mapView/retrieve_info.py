import subprocess, socket, json, time, threading, paramiko
from mapView.models import Node, Location, NodeLogStateRecords

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
	with open('mapView/config.json') as confi:
		data = json.load(confi)
	MASTER_NODE_IP = data['master_node']['ip']
	MASTER_NODE_PORT=data['master_node']['ssh_port']
	output=""

	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(MASTER_NODE_IP, MASTER_NODE_PORT, username='root', password='ungsmsmolsrd2', timeout=10)

	stdin, stdout, stderr = client.exec_command("echo \"/netjsoninfo filter graph ipv4_0\" | nc 127.0.0.1 9001")# a properties

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
	#for item in olsrObject.collection:
	if olsrObject.topology_id == 'ipv4_0':
		for node in olsrObject.nodes:
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
			#Gaurdar el registro de los nodos comp apagado
		if (node.node_ip in active_ips and node.node_states == 'ROJO'):
			node.node_states = 'VIOLETA'
			#Guardar el registro de los nodos como prendido

	#Esto no debería ir acá
	for node in nodes:
		print (node.node_ip, " | ", node.node_states)
		node.save()

def save_node_status():
	nodes = Node.objects.all()
	for node in nodes:
		if (node.node_states == 'ROJO'):
		#Guardar como apagado
			record = NodeLogStateRecords(record_node=node, record_node_state = 'APAGADO')
			record.save()
		else:
		#guardar como prendido
			record = NodeLogStateRecords(record_node=node, record_node_state = 'PRENDIDO')
			record.save()

def main(): #debería ser main
	while 1:
		try:
			raw_data = retrieve_info()
			node_info = json_to_object(json.loads(raw_data))
			save_changes(get_active_ips(node_info))

		except Exception:
			print("No se pude establecer conexión con el Nodo Maestros")
			#Avisarle al modelo que el Nodo Maestro está caído
			#Para ello, le decimos que todos los nodos de la red están cídos, incluyendo al NodoMaestro
			save_changes([])
			#Guardar el registro como apagado

		save_node_status()
		time.sleep(15)


def retrieve_info_daemon():
	d = threading.Thread(target=main, name='retrieve')
	d.setDaemon(True)
	d.start()
