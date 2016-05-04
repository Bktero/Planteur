""" This module provides classes to manipulate plants in the python world.
"""

import json
import logging

from enum import Enum

__author__ = 'pgradot'


class ConnectionType(Enum):
    network = 1
    wired = 2
    zigbee = 3


print(ConnectionType)
print(ConnectionType.wired)
print(ConnectionType['wired'])


class Plant(object):
    """A Plant is python object that represent a plant in the real world."""
    def __init__(self, uid, name):
        """Create a new plant.

        :param uid: a unique identifier of this plant
        :type uid: int
        :param name: the human-readable name of this plant
        :type name: str
        """
        self.uid = uid
        self.name = name

    def __str__(self):
        return '{}: uid={}, name={}'.format(self.__class__.__name__, self.uid, self.name)


class PlantLoader(object):
    """A PlantLoader loads a JSON description file and creates the corresponding
    set of plants.
    """
    def __init__(self, pathname):
        """Create a new loader.

        :param pathname: the pathname to the file that contains the descriptions of the plants
        :type pathname: str
        """
        self.pathname = pathname

    def __str__(self):
        return self.__class__.__name__ + ": " + self.pathname

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
                uid = index
                name = plant_dict["name"]
                plant = Plant(uid, name)
                logging.debug('Loading plant: %s', plant)
                plants.append(plant)

        return plants
