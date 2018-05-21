import logging
import time

import watering
from messaging import publish_plant_message, publish_ambient_message

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    sprinkler = watering.Sprinkler()
    sprinkler.start()

    time.sleep(1)

    publish_plant_message('pilea', 80, temperature=None)
    publish_plant_message('cactus', 50, 25)
    publish_plant_message('cocotier', humidity=None)

    publish_ambient_message('cellier', temperature=80, humidity=18)
    publish_ambient_message('living-room', humidity=None, temperature=18)
    publish_ambient_message('cave', humidity=None, temperature=None)
