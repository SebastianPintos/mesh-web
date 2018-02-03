import logging
import csv
from abc import ABC, abstractmethod

from logging.handlers import TimedRotatingFileHandler


class Logger:

    def __init__(self, path, periodicity):
        self.logger = logging.getLogger("log")
        self.logger.setLevel(logging.INFO)

        handler = TimedRotatingFileHandler(path, when=periodicity, interval=1, backupCount=10)

        self.logger.addHandler(handler)

    def write(self, string):
        self.logger.info(string)

    def log_csv(self, string_list):
        writer = csv.writer(self, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(string_list)


class UdpPackageLogger:

    def __init__(self):
        self.pkg_map = {0: Logger('/home/lucas/Mesh/log/amperage.csv', 'm'),
                        1: Logger('/home/lucas/Mesh/log/ardu_temp.csv', 'm'),
                        2: Logger('/home/lucas/Mesh/log/node_temp.csv', 'm')}

    def log_pkg(self, udp_pkg):
        type_pkg = udp_pkg.type
        logger = self.pkg_map[type_pkg]

        to_log = []

        for key in udp_pkg.__dict__:
            to_log.append(udp_pkg.__dict__[key])

        logger.log_csv(to_log)