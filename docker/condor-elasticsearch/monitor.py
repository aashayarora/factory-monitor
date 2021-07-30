#!/usr/bin/python
import aggregator.aggregator as aggregator
import messenger.messenger as messenger
import config.config as config
import logging
import os

def main():
	cfg = config.Config()

        # Create log file if it does not exist
        file = open(cfg.get_logfile_loc(), 'w+')
        file.close()
	logging.basicConfig(filename=cfg.get_logfile_loc(), format='%(asctime)s %(message)s', level=logging.DEBUG)

	def push_factory(factory):
		print("Current factory: " + str(factory["factory_name"]))
		influx_config_file = os.path.dirname(os.path.realpath(__file__)) + "/config/influxdb.json"
		#rabbitmq_config_file = os.path.dirname(os.path.realpath(__file__)) + "/config/rabbitmq.json"
                rabbitmq_config_osg_file = os.path.dirname(os.path.realpath(__file__)) + "/config/rabbitmq_osg.json"
		cfg.set_current_factory(factory)
		cfg_influx = cfg.build_inner_config(influx_config_file)
		#cfg_rabbit = cfg.build_inner_config(rabbitmq_config_file)
                cfg_rabbit_osg = cfg.build_inner_config(rabbitmq_config_osg_file)
		ag = aggregator.Aggregator(cfg_influx)
		msgr_influx = messenger.InfluxMessenger(cfg_influx)
		#msgr_rabbit = messenger.RabbitMessenger(cfg_rabbit)
                msgr_rabbit_osg = messenger.RabbitMessenger(cfg_rabbit_osg)
		log_debug("aggregating factory data")
		factory_data = ag.aggregate_factory_data()

		if factory_data is None:
			log_debug("factory data aggregation FAILED")
			return

		log_debug("factory data aggregation SUCCEEDED")
		try:
			msgr_influx.push_data(factory_data)
		except Exception as ex:
			print("Error in " + str(factory["factory_name"]) + "!")
			print("Could not push to Influx")
			print(ex)
		#try:
		#	msgr_rabbit.push_data(factory_data)
		#except Exception as ex:
		#	print("Error in " + str(factory["factory_name"]) + "!")
		#	print("Could not push to RabbitMQ")
		#	print(ex)
                try:
                        msgr_rabbit_osg.push_data(factory_data)
                except Exception as ex:
                        print("Error in " + str(factory["factory_name"]) + "!")
                        print("Could not push to RabbitMQ")
                        print(ex)
                

	for factory in cfg.get_factories():
		try:
			push_factory(factory)
		except Exception as ex:
			print("Error in " + str(factory["factory_name"]) + "!")
			print(ex)

def log_debug(msg):
	logging.debug("DEBUG: monitor.py: %s" % msg)

if __name__ == "__main__":
	main()
