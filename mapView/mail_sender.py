import configparser
import smtplib
from email.message import EmailMessage

class MailSender:
    def __init__(self, config_path):
        config = self.read_config_file(config_path)
        self.server_smtp = config['SMTPServer']
        self.port_smtp = config['SMTPPort']
        self.email = config['email']
        self.password = config['password']


    def read_config_file(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)

        return config['DEFAULT']

    def send_mail(self,receiver_email, subject, msg):
        message = EmailMessage()
        message.set_content(msg)
        
        message['Subject'] = subject
        message['From'] = self.email
        message['To'] = receiver_email
        
        s = smtplib.SMTP(self.server_smtp, self.port_smtp)
        s.starttls()
        s.login(self.email, self.password)
        s.send_message(message)
        s.quit()