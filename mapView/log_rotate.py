import logging
import csv
from abc import ABC, abstractmethod
from mapView.models import NodeLogCurrentRecords, NodeLogTemperatureRecords, Node

from logging.handlers import TimedRotatingFileHandler


class Logger:

    def __init__(self, logger, path, periodicity):
        self.logger = logging.getLogger(logger)
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
        self.pkg_map = {0: Logger('current', 'log/current.csv', 'd'),
                        1: Logger('ardu_temp', 'log/ardu_temp.csv', 'd'),
                        2: Logger('node_temp', 'log/node_temp.csv', 'd')}

    def log_pkg(self, udp_pkg):
        type_pkg = udp_pkg.type
        logger = self.pkg_map[type_pkg]

        to_log = []

        for key in udp_pkg.__dict__:
            to_log.append(udp_pkg.__dict__[key])

        print(to_log)
        logger.log_csv(to_log)

class UdpPackageSaver:

    def __init__(self):
        pass

    def save_pkg(self, udp_pkg):
        if udp_pkg.type == 0:
            self._save_current(udp_pkg)
        if udp_pkg.type == 1:
            self._save_temperature(udp_pkg)

    def _save_temperature(self, udp_pkg):
        node = Node.objects.get(pk=udp_pkg.ip)
        to_save = NodeLogTemperatureRecords(record_node=node,record_temperature=udp_pkg.values)
        to_save.save()

    def _save_current(self, udp_pkg):
        node = Node.objects.get(pk=udp_pkg.ip)
        to_save = NodeLogCurrentRecords(record_node=node,record_electric_current=udp_pkg.values)
        to_save.save()
