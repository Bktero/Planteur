import logging
import time

import watering
from monitoring import publish_plant_event, publish_ambient_event

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    sprinkler = watering.Sprinkler()
    sprinkler.start()

    time.sleep(1)

    publish_plant_event('pilea', 80, temperature=None)
    publish_plant_event('cactus', 50, 25)
    publish_plant_event('cocotier', humidity=None)

    publish_ambient_event('cellier', temperature=80, humidity=18)
    publish_ambient_event('living-room', humidity=None, temperature=18)
    publish_ambient_event('cave', humidity=None, temperature=None)
