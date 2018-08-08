import configparser

class MailSender:
    def __init__(self, config_path):
        config = self.read_config_file(config_path)
        self.server_smtp = config['SMTPServer']
        self.port_smtp = config['SMTPPort']
        self.email = config['email']
        self.password = config['password']

        print(self.email, self.password, self.port_smtp, self.server_smtp)

    def read_config_file(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)

        print(config)
        return config['DEFAULT']

    def send_email(receiver_email, subject, msg):
        pass
