import logging
import time

import database
import messaging

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    database_logger = database.DatabaseLogger('planteur.db')
    database_logger.start()

    time.sleep(1) # give some time to the database logger thread to connect to the MQTT server

    messaging.publish_plant_message('pilea', 80, temperature=None)  # will not trigger a watering request
    messaging.publish_plant_message('cactus', 50, 25)  # will trigger a watering request
    messaging.publish_plant_message('cocotier', humidity=None)  # cannot be published

    messaging.publish_ambient_message('cellier', humidity=18, temperature=80, )
    messaging.publish_ambient_message('living-room', humidity=None, temperature=18)
    messaging.publish_ambient_message('cave', humidity=75, temperature=None)
    messaging.publish_ambient_message('kitchen', humidity=None, temperature=None)  # cannot be published

    messaging.publish_watering_message('pilea')
    messaging.publish_watering_message('cactus')
