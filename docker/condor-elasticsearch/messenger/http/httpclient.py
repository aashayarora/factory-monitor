import urllib
import urllib2
import logging

class Client:
	def __init__(self, config):
		self.config = config

		self.database_url = config.get_database_url()
		if self.database_url is None:
			log_error("configuration file not set")

		self.database_name = config.get_database_name()
		if self.database_name is None:
			log_error("configuration file not set")

		self.database_password = config.get_database_password()
		if self.database_password is None:
			log_error("configuration file not set")

		self.database_username = config.get_database_username()
		if self.database_username is None:
			log_error("configuration file not set")

	def create_database(self, name):
		query = "CREATE DATABASE " + name
		url = self.database_url + "/query?"
		values = {'q': query,
			  'u': self.database_username,
			  'p': self.database_password }
		url += urllib.urlencode(values)
		req = urllib2.Request(url)
		resp = urllib2.urlopen(req)
		# TODO error handle

	def post(self, data):
		url = self.database_url + "/write?"
		values = {'db': self.database_name,
			  'precision': 's',
			  'u': self.database_username,
			  'p': self.database_password }
		url += urllib.urlencode(values)
		log_debug("sending data to: %s" % str(url))
		req = urllib2.Request(url, data)
		resp = urllib2.urlopen(req)

		if resp.getcode() < 200 or resp.getcode() > 299:
			log_error("sending data to database returned with an error: %s" % resp.getcode())
			return

		log_debug("response received: %s" % str(resp.getcode()))
		# TODO error handle
		
def log_debug(msg):
	logging.debug("DEBUG: httpclient.py: %s" % msg)

def log_error(msg):
	logging.error("ERROR: httpclient.py: %s" % msg)
