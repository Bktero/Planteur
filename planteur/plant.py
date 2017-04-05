""" This module provides classes to manipulate plants in the python world.
"""

import json
import logging

from enum import Enum

__author__ = 'pgradot'


class ConnectionType(Enum):
    """This enumeration provides the possible connection types between
    a plant peripheral and the Planteur gateway.
    """
    network = 1
    wired = 2
    xbee = 3


class WateringMethod(Enum):
    """This enumeration provides the possible watering methods for a plant."""
    planned = 1
    conditional = 2
    nowatering = 3


class Plant:
    """A Plant is python object that represent a plant from the real world."""
    def __init__(self, uid: str, name: str, connection: ConnectionType,watering: WateringMethod):
        """Create a new plant.

        :param uid: a unique identifier
        :param name: the human-readable name
        :param connection: the connection type
        :param watering: the watering method
        """
        self.uid = uid
        self.name = name
        self.connection = connection
        self.watering = watering

    def __str__(self):
        return '{}: uid={}, name={}, connection={} watering={}'.format(self.__class__.__name__, self.uid, self.name, self.connection, self.watering)


def load_plants_from_json(pathname: str):
    """Loads the set of plants described in a JSON file.

    Open the JSON description file represented by the pathname.
    Create a python object for each described plant.

    :param pathname: the pathname to the description file
    :return: a list of plants
    """
    plants = list()

    with open(pathname) as file:
        json_dict = json.load(file)

        for plant_dict in json_dict['plants']:
            # Extract data
            uid = plant_dict['uid']
            name = plant_dict['name']
            connection = ConnectionType[plant_dict['connection']]
            watering = WateringMethod[plant_dict['watering']]

            # Create plant and add it to the list of plants
            plant = Plant(uid, name, connection, watering)
            logging.debug('Loading plant: %s', plant)
            plants.append(plant)

            # Add special fields depending on the type of plant
            if plant.connection == ConnectionType.xbee:
                plant.xbee_id = plant_dict['xbee_id']

    return plants
