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
UDP_PORT = 14245


class App(object):
    """The Planteur application is here!"""

    def __init__(self, config_pathname, plant_pathname):
        """ Create a new application.

        :param config_pathname: the pathname to the configuration file
        :type config_pathname: str
        :param plant_pathname: the pathname to the plant description file
        :type plant_pathname: str
        """
        # Load configuration
        logging.info('Loading configuration...')
        self.config_pathname = config_pathname
        self._load_configuration()

        # Load plants
        logging.info('Logging plants...')
        loader = plant.PlantLoader(plant_pathname)
        self.plants = loader.load()

    def run(self):
        """Execute the application, just after it has been created."""
        logging.info('Planteur application starts')

        # Start monitor aggregator
        aggregator = monitoring.MonitoringAggregator()
        aggregator.start()

        # Start network adapter if there is at least one network plant
        for p in self.plants:
            if p.connection is plant.ConnectionType.network:
                network_adapter = monitoring.NetworkAdapter(aggregator, UDP_IPADDR, UDP_PORT)
                network_adapter.start()
                break

        # Start a wired adapter for each wired plant
        for p in self.plants:
            if p.connection is plant.ConnectionType.wired:
                wired_adapter = monitoring.StubWiredAdapter(aggregator, p.uid)
                wired_adapter.start()

        # TODO Start zigbee adapters

    def _load_configuration(self):
        with open(self.config_pathname) as file:
            json_dict = json.load(file)
            parameter = json_dict['category']['param']
            print(json_dict)
            print(parameter)
            parameter = json_dict['another_category']['other_param']
            print(parameter)


class StubNetworkPlant(object):

    def __init__(self, uid: str):
        self.uid = uid
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def emit(self):
        message = json.dumps({'uid': self.uid, 'humidity': random.randint(0, 100), 'temperature': random.randint(10, 30)})
        message_as_bytes = message.encode()
        self.sock.sendto(message_as_bytes, (UDP_IPADDR, UDP_PORT))


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    # Run Planteur
    app = App('config.json', 'plants.json')
    app.run()

    # Stub network plants
    tomatoes = StubNetworkPlant('pgt_tomatoes_network')
    ficus = StubNetworkPlant('pgt_ficus_network')
    plants = [tomatoes, ficus]

    while True:
        for p in plants:
            p.emit()
            time.sleep(2)
