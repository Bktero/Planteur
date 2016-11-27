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
    zigbee = 3


class WateringMethod(Enum):
    """This enumeration provides the possible watering methods for a plant."""
    planned = 1
    conditional = 2
    nowatering = 3


class Plant:
    """A Plant is python object that represent a plant from the real world."""
    def __init__(self, uid, name, connection, watering):
        """Create a new plant.

        :param uid: a unique identifier
        :type uid: str
        :param name: the human-readable name
        :type name: str
        :param connection: the connection type
        :type connection: ConnectionType
        :param watering: the watering method
        :type watering: WateringMethod
        """
        self.uid = uid
        self.name = name
        self.connection = connection
        self.watering = watering

    def __str__(self):
        return '{}: uid={}, name={}, connection={} watering={}'.format(self.__class__.__name__, self.uid, self.name, self.connection, self.watering)


class PlantLoader:
    """A PlantLoader loads a JSON description file and creates the corresponding
    set of plants.
    """
    def __init__(self, pathname):
        """Create a new loader.

        :param pathname: the pathname to the description file
        :type pathname: str
        """
        self.pathname = pathname

    def __str__(self):
        return '{}: pathname={}'.format(self.__class__.__name__ , self.pathname)

    def load(self):
        """Load the plants.

        Open the JSON description file represented by the pathname.
        Create a python object for each described plant.

        :return: the list of these objects
        """
        plants = []
        with open(self.pathname) as file:
            json_dict = json.load(file)
            for index, plant_dict in enumerate(json_dict['plants']):
                uid = plant_dict['uid']
                name = plant_dict['name']
                connection = ConnectionType[plant_dict['connection']]
                watering = WateringMethod[plant_dict['watering']]
                plant = Plant(uid, name, connection, watering)
                logging.debug('Loading plant: %s', plant)
                plants.append(plant)

        return plants
