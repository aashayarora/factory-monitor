import os
import json

class Config:
	class InnerConfig:
		# TODO Decide if a getter for every different attribute of the
		# config object is better that a single getter.
		def __init__(self, file):
			with open(file) as config_file:
				self.data = json.load(config_file)

		def get(self, attribute):
			if self.data[attribute] == "":
				return None
			return self.data[attribute]

		def set(self, attribute, value):
			self.data[attribute] = value

		def set_current_factory_name(self, current_factory_name):
			self.data['factory_name'] = current_factory_name

		def set_schedd_url(self, schedd_url):
			self.data['schedd_url'] = schedd_url

		def set_completed_url(self, completed_url):
			self.data['completed_url'] = completed_url

		def get_database_url(self):
			if self.data['database_URL'] == "":
				return None
			return self.data['database_URL']

		def get_database_username(self):
			if self.data['username'] == "":
				return None
			return self.data['username']

		def get_database_password(self):
			if self.data['password'] == "":
				return None
			return self.data['password']

		def get_database_name(self):
			if self.data['database_name'] == "":
				return None
			return self.data['database_name']

		def get_measurement_name(self):
			if self.data['measurement_name'] == "":
				return None
			return self.data['measurement_name']

		def get_current_factory_name(self):
			if self.data['factory_name'] == "":
				return None
			return self.data['factory_name']

		def get_schedd_url(self):
			if self.data['schedd_url'] == "":
				return None
			return self.data['schedd_url']

		def get_completed_url(self):
			if self.data['completed_url'] == "":
				return None
			return self.data['completed_url']

		def get_logfile_loc(self):
			return os.path.dirname(os.path.realpath(__file__)) + self.data['logfile_loc']

		def get_monitor_dir(self):
			return os.path.dirname(os.path.realpath(__file__)) + self.data['monitor_dir']

		def get_rabbitmq_host(self):
			if self.data['host'] == "":
				return None
			return self.data['host']

		def get_rabbitmq_user(self):
			if self.data['username'] == "":
				return None
			return self.data['username']

		def get_rabbitmq_password(self):
			if self.data['password'] == "":
				return None
			return self.data['password']

		def get_rabbitmq_queue(self):
			if self.data['queue'] == "":
				return None
			return self.data['queue']

		def get_rabbitmq_exchange(self):
			if self.data['exchange'] == "":
				return none
			return self.data['exchange']

		def get_rabbitmq_key(self):
			if self.data['key'] == "":
				return none
			return self.data['key']


	def __init__(self):
		config_file = os.path.dirname(os.path.realpath(__file__)) + "/config.json"
		with open(config_file) as f:
			self.data = json.loads(f.read())
		try:
			self.set_current_factory(self.data['factories'][0])
		except:
			print("No factories configured")

	def set_current_factory(self, factory):
		# factory is a dictionary with keys factory_name, schedd_url and completed_url
		self.current_factory = factory

	def get_factories(self):
		return self.data['factories']

	def build_inner_config(self, config_file):
		config = Config.InnerConfig(config_file)
		config.data['logfile_loc'] = self.data['logfile_loc']
		config.data['monitor_dir'] = self.data['monitor_dir']
		config.set("factory_name", self.current_factory['factory_name'])
		config.set("schedd_url", self.current_factory['schedd_url'])
		config.set("completed_url", self.current_factory['completed_url'])
		return config

	def get_logfile_loc(self):
		return os.path.dirname(os.path.realpath(__file__)) + self.data['logfile_loc']

	def get_monitor_dir(self):
		return os.path.dirname(os.path.realpath(__file__)) + self.data['monitor_dir']

