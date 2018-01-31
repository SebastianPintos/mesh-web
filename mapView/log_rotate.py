import logging
import time

from logging.handlers import TimedRotatingFileHandler

class Logger:
	
	def __init__(self, path, periodicity):
		self.logger=logging.getLogger("Changeme")
		self.logger.setLevel(logging.INFO)
		
		handler = TimedRotatingFileHandler(path, when=periodicity, interval=1, backupCount=5)
		
		self.logger.addHandler(handler)

		
	def log(self, string):
		self.logger.info(string)

