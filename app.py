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
        logging.info('Planteur application starts')

        # Load configuration and plants
        self._load_configuration()
        self._load_plants()

        # Start monitoring adapters
        network_adapter = monitoring.NetworkMonitoringAdapter(UDP_IPADDR, UDP_PORT)
        network_adapter.start()

        wired_adapter = monitoring.StubWiredAdapter()
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
        plants = loader.load()
        print(plants)

if __name__ == '__main__':
    app = App('config.json', 'plants.json')
    app.run()

    # Stub for plants that are connected to the network
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        message = 'Plant: network id={}, humidity={}'.format("ae1256", random.randint(0, 100))
        message_as_bytes = message.encode()
        sock.sendto(message_as_bytes, (UDP_IPADDR, UDP_PORT))
        time.sleep(2)

