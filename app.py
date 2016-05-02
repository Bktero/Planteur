"""
This is the entry point for the Planteur application.
"""
import json
import logging

__author__ = 'pgradot'

# Application startup
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                    level=logging.INFO)

# Main work
logging.info('Planteur application starts')

logging.info('Loading configuration...')
with open('config.json') as file:
    dict = json.load(file)
    parameter = dict['category']['param']
    print(dict)
    print(parameter)
    parameter = dict['another_category']['other_param']
    print(parameter)

logging.warning('Planteur application ends')