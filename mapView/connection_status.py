import subprocess
import schedule, time, json
from mapView.mail_sender import MailSender

def detect_connection(ip_address, intents):
    procces = subprocess.run(['ping', '-c', str(intents), ip_address], shell=False, stdout=subprocess.PIPE)
    return procces.returncode is 0

def print_traceroute(ip_address):
    procces = subprocess.run(['traceroute', ip_address], shell=False, stdout=subprocess.PIPE)
    return str(procces.stdout)

def is_time_exceeded(node ,exceeded_time):
    last_register = NodeLogCurrentRecords.objects.filter(record_node = node).last().record_date
    actual_date = datetime.now()
    
    actual_date = actual_date.replace(tzinfo=utc)
    last_register = last_register.replace(tzinfo=utc)   #FIXME Si confiaramos en los estados, esto debería preguntar el estado, y si es violeta, directamente notificarlo
    
    difference = last_register - node_date
    
    print(difference)

def main():
    mail_sender = MailSender("../email_settings.ini")
    with open('config.json') as confi:
        data = json.load(confi)
    
    print(data['master_node']['ip']) #TODO Reemplazar Data en detect_connection
    
    if(not detect_connection("192.168.3.2", 2)):
        mail_sender.send_mail("lucas.addisi@gmail.com", "Test", print_traceroute("www.google.com"))#TODO Reemplazar Data en detect_connection
    else:
        print("Se detectó conectividad")


def scan_connectivity_job():
    schedule.every().day.at("12:33c").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)