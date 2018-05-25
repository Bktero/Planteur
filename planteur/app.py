""" This is the entry point for the Planteur application."""
import json
import logging
from collections import namedtuple

import serial

import adapters
import database
import plant
import watering


def _configure_logging(config_pathname):
    logging.info('Loading configuration...')

    with open(config_pathname) as file:
        # Load JSON content
        json_dict = json.load(file)

        # Log level
        level_str = json_dict['log']['level']
        level = getattr(logging, level_str.upper())
        logging.info('Changing log level to %s', level)
        logging.getLogger().setLevel(level)

        # XBee port


def _start_xbee_adapter(config_pathname, plants):
    # Check that there if there is at least one network plant
    xbee_ids_to_uids = dict()
    for plant_ in plants:
        if plant_.connection is plant.ConnectionType.xbee:
            xbee_ids_to_uids[plant_.xbee_id] = plant_.uid

    logging.debug('XBee ID <==> UID: %s', xbee_ids_to_uids)

    if len(xbee_ids_to_uids) != 0:
        # Get XBee port from configuration
        with open(config_pathname) as file:
            json_dict = json.load(file)
            xbee_port = json_dict['xbee']['serial_port']

        # Open port
        ser = serial.Serial(xbee_port)

        # Start adapter
        xbee_adapter = adapters.XbeeAdapter(ser, xbee_ids_to_uids)
        xbee_adapter.start()


def planteur(config_pathname, plant_pathname):
    """Run the Planteur :)

    :param config_pathname: the pathname to the configuration file
    :type config_pathname: str
    :param plant_pathname: the pathname to the plant description file
    :type plant_pathname: str
    """
    logging.info('Planteur application starts')
    _configure_logging(config_pathname)

    # Load plants
    logging.info('Loading plants...')
    plants = plant.load_plants_from(plant_pathname)
    if len(plants) == 0:
        logging.warning('No plant has been loaded, plants.json may be empty')

    # Start database logger
    db_logger = database.DatabaseLogger('planteur.db')
    db_logger.start()

    # Start sprinkler
    sprinkler = watering.Sprinkler(plants)
    sprinkler.start()

    # TODO create watering planner if at least one plant as 'planned' as it's watering method

    # Start adapters
    _start_xbee_adapter(config_pathname, plants)

    # TODO create and start custom adapters

    # Startup complete
    logging.debug('Application startup is complete')


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    # Run Planteur
    planteur('config.json', 'plants.json')
