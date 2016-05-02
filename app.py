"""
This is the entry point for the Planteur application.
"""
import logging

__author__ = 'pgradot'

# Application startup
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                    level=logging.INFO)

# Main work
logging.info('Planteur application starts')

logging.warning('Planteur application ends')