import logging
import os
from http import httpclient
import pika
import time
import json
import random

class Messenger:
	def __init__(self, config):
		self.config = config
		self.httpclient = httpclient.Client(config)

		self.measurement_name = config.get_measurement_name()
		if self.measurement_name is None:
			log_error("configuration file not set")

		self.database_name = config.get_database_name()
		if self.database_name is None:
			log_error("configuration file not set")

		self.current_factory = config.get_current_factory_name()
		if self.current_factory is None:
			log_error("configuration file not set")

		self.dir_path = os.path.dirname(os.path.realpath(__file__))

class InfluxMessenger(Messenger):
	def __init__(self, config):
		Messenger.__init__(self,config)

	def push_data(self, factory_data):

		# save factory_data to outbox file
		log_debug("saving factory data to outbox")
		self.save_to_outbox(factory_data)

		# create database
		self.httpclient.create_database(self.database_name)

		# send outbox file to influx
		log_debug("pushing factory data to database")
		print("Pushed to influx")
		self.push_outbox()

	def save_to_outbox(self, factory_data):
		try:
			# write data to file
			f = None
			f = open(self.dir_path + '/outbox/outbox.txt', 'w')

			factory_fragment = "factory=" + self.current_factory

			for entry_name, entry_data in factory_data.items():
			
				entry_fragment = "entryname=" + entry_name

				for frontend_name, frontend_data in entry_data.items():
					frontend_fragment = "frontendname=" + frontend_name + " "

					metric_fragment = ""
					for metric_name, metric_data in frontend_data.items():
						metric_fragment += str(metric_name) + "=" + str(metric_data) + ","
					line = self.measurement_name + "," + \
						factory_fragment + "," + \
						entry_fragment + "," + \
						frontend_fragment + " " + \
						metric_fragment[:-1] + \
						"\n"
					f.write(line)
		except IOError as e:
			log_error(str(e))
		finally:
			if f is not None:
				f.close()

	def push_outbox(self):
		try:
			f = None
			f = open(self.dir_path + '/outbox/outbox.txt')
			fragment = "\n".join([line for line in f])
			fragment = fragment.replace("\n\n", "\n")
			self.httpclient.post(fragment)
		except IOError as e:
			log_error(str(e))
		finally:
			if f is not None:
				f.close()

class RabbitMessenger(Messenger):
	def __init__(self, config):
		#Messenger.__init__(self,config)
		self.current_factory = config.get_current_factory_name()
		if self.current_factory is None:
			log_error("configuration file not set")
		self.dir_path = os.path.dirname(os.path.realpath(__file__))
		self.outbox_filename = self.dir_path + '/outbox/outbox_' + self.current_factory + '.txt'
		self.rabbitmq_host = config.get("host")
		self.rabbitmq_user = config.get("username")
		self.rabbitmq_password = config.get("password")
		self.rabbitmq_queue = config.get("queue")
		self.rabbitmq_exchange = config.get("exchange")
		self.rabbitmq_key = config.get("key")
		self.rabbitmq_vhost = config.get("vhost")
	
	def push_data(self, factory_data):
		# save factory_data to outbox file as ES bulk query
		log_debug("saving factory data to outbox")
		self.save_to_outbox(factory_data)
		# Set up conection with RabbitMQ
		host = self.rabbitmq_host
		vhost = self.rabbitmq_vhost
		print("vhost is {}".format(self.rabbitmq_vhost))
	
		credentials = pika.PlainCredentials(self.rabbitmq_user,self.rabbitmq_password)
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,credentials=credentials, virtual_host=vhost))
		self.channel = connection.channel()
		self.channel.queue_declare(queue=self.rabbitmq_queue)
		
		# send outbox file to RabbitMQ
		log_debug("pushing factory data to message broker")
		self.push_outbox()
		connection.close()
		print("Pushed to Rabbit")

	def save_to_outbox(self, factory_data):
		message_list = list()
		# Build each message as a dict.
		milis_epoch = int(time.time()*1000)
		for entry_name, entry_data in factory_data.items():
			for frontend_name, frontend_data in entry_data.items():
				log_data = dict()
				log_data['entryname'] = entry_name
				log_data['factory'] = self.current_factory
				log_data['frontendname'] = frontend_name
				for metric_name, metric_data in frontend_data.items():
					# Check if data is integer, if so, obtain integer
					try:
						metric_data_cast = int(metric_data)
						metric_data = metric_data_cast
					except:
						pass
					log_data[str(metric_name)] = metric_data
 				# TODO Change the source of the time to the one in the metrics.
				# Milliseconds since epoch for ES	
				log_data['time'] = milis_epoch
				message_list.append(log_data)
				#print(log_data)
		# Build json string.
		messages = ""
		for log in message_list:
			#messages += '{ "index" : { "_index" : "logged_stats", "_type": "doc" } }'
			messages += '\n' + json.dumps(log) + '\n'
		try:
			# write data to file
			f = None
			f = open(self.outbox_filename, 'w')
			f.write(messages)

		except IOError as e:
			log_error(str(e))
		finally:
			if f is not None:
				f.close()

	def push_outbox(self):
		try:
			f = None
			f = open(self.outbox_filename)
                        message = ""
                        for line in f:
                            message += line + '\n'
			message = message.replace("\n\n", "\n")
			message_single = message.split("\n")
			exchange = self.rabbitmq_exchange
			key = self.rabbitmq_key
			self.channel.exchange_declare(exchange=exchange, exchange_type='fanout',durable=True)
			for one_message in message_single:
				self.channel.basic_publish(exchange=exchange, routing_key=key, body=one_message)
				#print(one_message)	

		except IOError as e:
			log_error(str(e))
		finally:
			if f is not None:
				f.close()
			# The file was sent correctly, erase the contents
			open(self.outbox_filename, 'w').close()

def log_debug(msg):
	logging.debug("DEBUG: messenger.py: %s" % msg)

def log_error(msg):
	logging.error("ERROR: messenger.py: %s" % msg)
