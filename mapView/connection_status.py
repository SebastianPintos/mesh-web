import subprocess
import schedule, time, json, pytz
from datetime import datetime, timedelta
from mapView.mail_sender import MailSender
from mapView.models import NodeLogCurrentRecords

def detect_connection(ip_address, intents):
    procces = subprocess.run(['ping', '-c', str(intents), ip_address], shell=False, stdout=subprocess.PIPE)
    return procces.returncode is 0

def print_traceroute(ip_address):
    procces = subprocess.run(['traceroute', ip_address], shell=False, stdout=subprocess.PIPE)
    return str(procces.stdout)

def is_time_exceeded(node, excedeed_time): 
        expected_time = timedelta(minutes=excedeed_time)

        utc=pytz.UTC

        actual_date = datetime.now()
        node_date = NodeLogCurrentRecords.objects.filter(record_node = node).last().record_date


        actual_date = actual_date.replace(tzinfo=utc)
        node_date = node_date.replace(tzinfo=utc)

        difference = actual_date - node_date
        print("La difrencia con el último registro de ", node.node_ip, " es: ", difference)

        return difference > expected_time

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
    schedule.every().day.at("12:33").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)