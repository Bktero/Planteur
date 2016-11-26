""" This module provides classes to manipulate plants in the python world.
"""

import json
import logging

from enum import Enum

__author__ = 'pgradot'


class ConnectionType(Enum):
    """This enumeration provides the possible connection mediums between
    a plant peripheral and the Planteur gateway.
    """
    network = 1
    wired = 2
    zigbee = 3


class Plant(object):
    """A Plant is python object that represent a plant from the real world."""
    def __init__(self, uid, name, connection):
        """Create a new plant.

        :param uid: a unique identifier of this plant
        :type uid: str
        :param name: the human-readable name of this plant
        :type name: str
        :param connection: the connection type to this plant
        :type connection: ConnectionType
        """
        self.uid = uid
        self.name = name
        self.connection = connection

    def __str__(self):
        return '{}: uid={}, name={}, connection={}'.format(self.__class__.__name__, self.uid, self.name, self.connection)


class PlantLoader(object):
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
        return "{}: pathname={}".format(self.__class__.__name__ , self.pathname)

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
                uid = plant_dict["uid"]
                name = plant_dict["name"]
                connection = ConnectionType[plant_dict["connection"]]
                plant = Plant(uid, name, connection)
                logging.debug('Loading plant: %s', plant)
                plants.append(plant)

        return plants
