import subprocess, json, time, threading

def init_tunnel():

	process1 = subprocess.run(['ssh', '-nNT', '-L', '8082:192.168.1.1:9001', 'root@192.168.1.1'])

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

	while 1:
		LOCAL_IP = '192.168.1.1'
		LOCAL_PORT='9001'

		process1 = subprocess.Popen(['echo', '/netjsoninfo graph'], stdout=subprocess.PIPE)

		process2 = subprocess.run(['nc', LOCAL_IP, LOCAL_PORT], stdin=process1.stdout, stdout=subprocess.PIPE)

		result = process2.stdout.decode('utf-8')

		print (result)

		time.sleep(5)
	return result	

def save_changes(): #debería ser main
	raw_data = retrieve_info()
	node_info = json_to_object(json.loads(raw_data))

	#guardar cambios
	return node_info

def retrieve_info_daemon():
	d = threading.Thread(target=retrieve_info, name='retrieve')
	d.setDaemon(True)
	d.start()