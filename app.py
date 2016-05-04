""" This is the entry point for the Planteur application."""
import json
import logging
import random
import socket
import time

import monitoring

import plant

__author__ = 'pgradot'

UDP_IPADDR = 'localhost'
UDP_PORT = 4245


class App(object):
    """The Planteur application is here!"""

    def __init__(self, config_pathname, plant_pathname):
        """ Create a new application.

        :param config_pathname: the pathname to the configuration file
        :type config_pathname: str
        :param plant_pathname: the pathname to the plant description file
        :type plant_pathname: str
        """
        self.config_pathname = config_pathname
        self.plant_pathname = plant_pathname

        # Default configuration for logging
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    def run(self):
        """Execute the application, just after it has been created."""
        logging.info('Planteur application starts')

        # Load configuration and plants
        self._load_configuration()
        self._load_plants()

        # Start monitoring adapters and their aggregator
        aggregator = monitoring.MonitoringAggregator()
        aggregator.start()

        network_adapter = monitoring.NetworkMonitoringAdapter(aggregator, UDP_IPADDR, UDP_PORT)
        network_adapter.start()

        wired_adapter = monitoring.StubWiredAdapter(aggregator, 'pgt_bonzai_wired')
        wired_adapter.start()

    def _load_configuration(self):
        logging.info('Loading configuration...')
        with open(self.config_pathname) as file:
            json_dict = json.load(file)
            parameter = json_dict['category']['param']
            print(json_dict)
            print(parameter)
            parameter = json_dict['another_category']['other_param']
            print(parameter)

    def _load_plants(self):
        loader = plant.PlantLoader('plants.json')
        print(loader)
        loaded_plants = loader.load()
        print(str(loaded_plants))


class StubNetworkPlant(object):

    def __init__(self, uid: str):
        self.uid = uid
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def emit(self):
        message = json.dumps({'uid': self.uid, 'humidity': random.randint(0, 100), 'temperature': random.randint(10, 30)})
        message_as_bytes = message.encode()
        self.sock.sendto(message_as_bytes, (UDP_IPADDR, UDP_PORT))


if __name__ == '__main__':
    app = App('config.json', 'plants.json')
    app.run()

    # Stub network plants
    tomatoes = StubNetworkPlant("pgt_tomatoes_1")
    ficus = StubNetworkPlant("pgt_ficus_elastica_1")
    plants = [tomatoes, ficus]
    while True:
        for plant in plants:
            plant.emit()
            time.sleep(2)
