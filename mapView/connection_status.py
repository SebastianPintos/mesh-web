import subprocess

def detect_connection(ip_address, intents):
    procces = subprocess.run(['ping', '-c', str(intents), ip_address], shell=False, stdout=subprocess.PIPE)
    return procces.returncode is 0

def print_traceroute(ip_address):
    procces = subprocess.run(['traceroute', ip_address], shell=False, stdout=subprocess.PIPE)
    return procces.stdout
