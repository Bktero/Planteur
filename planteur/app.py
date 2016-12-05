""" This is the entry point for the Planteur application."""
import json
import logging
import random
import socket
import time

import database
import monitoring
import plant
import watering

__author__ = 'pgradot'

UDP_IPADDR = 'localhost'
UDP_PORT = 14246


def planteur(config_pathname, plant_pathname):
    """Run the Planteur!

    :param config_pathname: the pathname to the configuration file
    :type config_pathname: str
    :param plant_pathname: the pathname to the plant description file
    :type plant_pathname: str
    """
    logging.info('Planteur application starts')

    # Load configuration
    logging.info('Loading configuration...')
    with open(config_pathname) as file:
        # Log level
        json_dict = json.load(file)
        level_str = json_dict['log']['level']

        level = getattr(logging, level_str.upper())

        logging.info('Changing log level to %s', level)
        logging.getLogger().setLevel(level)

    # Load plants
    logging.info('Logging plants...')
    plants = plant.load_plants_from_json(plant_pathname)

    # Create sprinkler, monitoring aggregator and database storer
    storer = database.DatabaseStorer('planteur.db')

    sprinkler = watering.Sprinkler(plants)
    sprinkler.listeners.append(storer)

    aggregator = monitoring.MonitoringAggregator(plants)
    aggregator.listeners.append(storer)
    aggregator.listeners.append(sprinkler)

    # TODO create watering planner

    aggregator.start()
    sprinkler.start()

    # Start network adapter if there is at least one network plant
    for plant_ in plants:
        if plant_.connection is plant.ConnectionType.network:
            network_adapter = monitoring.NetworkAdapter(aggregator, UDP_IPADDR, UDP_PORT)
            network_adapter.start()
            break

    # Start a wired adapter for each wired plant
    for plant_ in plants:
        if plant_.connection is plant.ConnectionType.wired:
            wired_adapter = monitoring.StubWiredAdapter(aggregator, plant_.uid)
            wired_adapter.start()

    # TODO start zigbee adapters


class StubNetworkPlant(object):
    """A stub plant that communicate thought network with UPD."""
    def __init__(self, uid: str):
        self.uid = uid
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.humidity = 0

    def send_data(self):
        """ Send a UDP datagram with generate stub data."""
        self.humidity += 1
        if self.humidity > 100:
            self.humidity = 0

        # self.humidity = random.randint(0, 100)

        message = json.dumps({'plant':
                                  {
                                      'uid': self.uid,
                                      'humidity': self.humidity,
                                      'temperature': random.randint(10, 30)
                                  }
                              })

        message_as_bytes = message.encode()
        self.sock.sendto(message_as_bytes, (UDP_IPADDR, UDP_PORT))


def stub_plant_activity():
    """Simulate plant activity through network."""
    tomatoes = StubNetworkPlant('pgt_tomatoes_network')
    ficus = StubNetworkPlant('pgt_ficus_network')
    plants = [tomatoes, ficus]

    while True:
        for plant_ in plants:
            plant_.send_data()
            time.sleep(1)

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    # Run Planteur
    planteur('config.json', 'plants.json')


    # Simulate plant activity
    stub_plant_activity()
