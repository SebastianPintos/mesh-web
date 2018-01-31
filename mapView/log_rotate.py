import logging
import time
import csv

from logging.handlers import TimedRotatingFileHandler

class Logger:

	def __init__(self, path, periodicity):
		self.logger=logging.getLogger("Changeme")
		self.logger.setLevel(logging.INFO)

		handler = TimedRotatingFileHandler(path, when=periodicity, interval=1, backupCount=5)

		self.logger.addHandler(handler)

	def write(self, string):
		self.logger.info(string)

	def log_csv(self, string_list):
		writer = csv.writer(self, delimiter=',', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(string_list)
