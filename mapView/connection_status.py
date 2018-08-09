import subprocess
import schedule, time, json
from mail_sender import MailSender

def detect_connection(ip_address, intents):
    procces = subprocess.run(['ping', '-c', str(intents), ip_address], shell=False, stdout=subprocess.PIPE)
    return procces.returncode is 0

def print_traceroute(ip_address):
    procces = subprocess.run(['traceroute', ip_address], shell=False, stdout=subprocess.PIPE)
    return str(procces.stdout)

def main():
    mail_sender = MailSender("../email_settings.ini")
    with open('config.json') as confi:
        data = json.load(confi)
    
    print(data['master_node']['ip']) #TODO Reemplazar Data en detect_connection
    
    if(not detect_connection("192.168.0.10", 2)):
        mail_sender.send_mail("lucas.addisi@gmail.com", "Test", print_traceroute("192.168.0.10"))
    else:
        print("Se detectó conectividad")


def scan_connectivity_job():
    #schedule.every().day.at("00:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)