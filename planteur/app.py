""" This is the entry point for the Planteur application."""
import json
import logging

import serial

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

    # Read configuration
    logging.info('Loading configuration...')
    with open(config_pathname) as file:
        # Load JSON content
        json_dict = json.load(file)

        # Log level
        level_str = json_dict['log']['level']
        level = getattr(logging, level_str.upper())
        logging.info('Changing log level to %s', level)
        logging.getLogger().setLevel(level)

        # XBee serial port
        xbee_serial_port = json_dict['xbee']['serial_port']

    # Load plants
    logging.info('Loading plants...')
    plants = plant.load_plants_from_json(plant_pathname)
    if len(plants) == 0:
        logging.warning('No plant has been loaded, plants.json may be empty')

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

    # Start an XBee adapter if there is at least one network plant
    xbee_uids = dict()
    for plant_ in plants:
        if plant_.connection is plant.ConnectionType.xbee:
            xbee_uids[plant_.xbee_id] = plant_.uid

    if len(xbee_uids) != 0:
        ser = serial.Serial(xbee_serial_port)
        logging.debug('XBee ID <==> UID: %s', xbee_uids)
        xbee_adapter = monitoring.XBeeAdapter(aggregator, ser, xbee_uids)
        xbee_adapter.start()

    # Start a wired adapter for each wired plant
    # FIXME replace with custom class loading
    for plant_ in plants:
        if plant_.connection is plant.ConnectionType.wired:
            wired_adapter = monitoring.StubWiredAdapter(aggregator, plant_.uid)
            # wired_adapter.start()

    # Startup complete
    logging.debug('Application startup is complete')


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    # Run Planteur
    planteur('config.json', 'plants.json')
