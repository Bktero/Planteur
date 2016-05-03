""" This is the entry point for the Planteur application."""
import json
import logging

import plant

__author__ = 'pgradot'


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

        # Load configuration from configuration file
        self._load_configuration()

        # Load plants from description file
        self._load_plants()

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
