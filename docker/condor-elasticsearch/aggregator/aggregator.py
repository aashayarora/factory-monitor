import logging
import json
import urllib2
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

SCHEDD_STATUS_FILE = "schedd_status.xml"
COMPLETED_DATA_FILE = "completed_data.json"

# TODO abstract xml parsing from aggregator
# TODO add time to the agregator
class Aggregator:
	def __init__(self, config):
		self.config = config
		self.monitor_dir = config.get_monitor_dir()

	def aggregate_factory_data(self):
		schedd_filename = self.monitor_dir + SCHEDD_STATUS_FILE
		completed_filename = self.monitor_dir + COMPLETED_DATA_FILE

		schedd_url = self.config.get_schedd_url()
		completed_url = self.config.get_completed_url()

		# aggregate schedd_status
		schedd_status_data = self.aggregate_schedd_data(schedd_url)
		if schedd_status_data is None:
			log_error("schedd_status_data returned None")
			return None
		log_debug("successfully aggregated schedd_status")

		# aggregate completed_data
		completed_data = self.aggregate_completed_data(completed_url)
		if completed_data is None:
			log_error("completed_data returned None")
			return None
		log_debug("successfully aggregated completed_data")

		merged_dicts = merge_dicts([schedd_status_data, completed_data])

		return merged_dicts

	def aggregate_completed_data(self, completed_url):
		factory_data = dict()
		completed_data = dict()
		try:
                        completed_data_fp = urllib2.urlopen(completed_url)
			completed_data = json.load(completed_data_fp)
		except IOError as e:
			log_error(str(e))
			return None
		finally:
			completed_data_fp.close()
    
		entries = completed_data['stats']['entries']
		for entry_name in entries:
			entry_data = dict()
			frontends = entries[entry_name]['frontends']
			for frontend_name in frontends:
				frontend_data = dict()
				for metric, value in frontends[frontend_name]['completed']['stats'].items():
					frontend_data['completed_' + metric] = value
				for metric, value in frontends[frontend_name]['completed_stats']['stats'].items():
					frontend_data['completed_stats_' + metric] = value
				for metric, value in frontends[frontend_name]['completed_wastetime']['stats'].items():
					frontend_data['completed_wastetime_' + metric] = value
				entry_data[frontend_name] = frontend_data
			factory_data[entry_name] = entry_data
		return factory_data

	def aggregate_schedd_data(self, schedd_url):
		factory_data = dict()

		# Event based iteration
		schedd_data = urllib2.urlopen(schedd_url)
		xml_iterator = iter(ET.iterparse(file=schedd_data, events=("start", "end")))

		# go through all entries
        	for event, elem in xml_iterator:
			# save data for each entry we encounter...
                	if event == 'start' and elem.tag == 'entry':
				entry_data = dict()
				entry_name = elem.get("name")
				if entry_name is None:
					log_error("Malformed XML: an entry does not have a name attribute")
					return None
			# skip totals for each entry
			elif event == 'start' and elem.tag == 'total':
				while(event != 'end' or elem.tag != 'total'):
					event, elem = xml_iterator.next()

			# save data for each frontend we encounter...
			elif event == 'start' and elem.tag == 'frontend':
				frontend_data = dict()
				frontend_name = elem.get("name") 
				if frontend_name is None:
					log_error("Malformed XML: frontend in entry %s does not have a name attribute" % entry_name)
					return None

			elif event == 'start' and elem.tag == 'ClientMonitor':
					for metric, value in elem.items():
						frontend_data["client_" + metric] = value
			elif event == 'start' and elem.tag == 'Requested':
					for metric, value in elem.items():
						frontend_data["requested_" + metric] = value
			elif event == 'start' and elem.tag == 'Status':
					for metric, value in elem.items():
						frontend_data["status_" + metric] = value

			elif event == 'end' and elem.tag == 'frontend':
				entry_data[frontend_name] = frontend_data
				elem.clear()

			# ...until we reach the end of all frontends for this entry
			elif event == 'end' and elem.tag == 'frontends':
				factory_data[entry_name] = entry_data
				elem.clear()

			# ...until we reach the end of all entries for this factory
			elif event == 'end' and elem.tag == 'entries':
				elem.clear()
				return factory_data
			else:
                		elem.clear()

def log_debug(msg):
	logging.debug("DEBUG: aggregator.py: %s" % msg)

def log_error(msg):
	logging.error("ERROR: aggregator.py: %s" % msg)

def merge_dicts(dicts):
	if len(dicts) <= 1:
		return dicts

	master_dict = dict()

	for d in dicts:
		for entry_name, entry_data in d.items():
			for frontend_name, frontend_data in entry_data.items():
				try:
					master_dict[entry_name][frontend_name].update(frontend_data)
				except KeyError:
					try:
						master_dict[entry_name][frontend_name] = frontend_data
					except KeyError:
						master_dict[entry_name] = dict()
						master_dict[entry_name][frontend_name] = frontend_data
							
	return master_dict

