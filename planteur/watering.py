"""This modules provides classes for watering."""

import logging
import queue
import threading
import json
import paho.mqtt.publish


def publish_watering_request(uid):
    """Publish a message to the 'planteur/watering' topic.

    :param uid: the UID of the plant
    """
    d = dict()
    d['watering'] = dict()
    d['watering']['uid'] = uid

    message = json.dumps(d)
    logging.info('Publish watering request: %s', message)
    paho.mqtt.publish.single('planteur/watering', message)


class Sprinkler:
    def __init__(self):
        self.client = paho.mqtt.client.Client()

    def start(self):
        """Start the sprinkler thread."""
        name = '{} thread'.format(self.__class__.__name__)
        thread = threading.Thread(target=self._run, name=name)
        thread.start()

    def _run(self):
        """Receive and process MQTT messages."""

        def on_connect(client, userdata, flags, rc):
            logging.info('%s: connected with result %s', self.__class__.__name__, str(rc))
            client.subscribe('planteur/plant')

        def on_message(client, userdata, message):
            logging.debug('%s: new message %s', self.__class__.__name__, message.payload)

            # Note: Paho receives strings on Xubuntu but bytes on Raspberry
            # mosquitto_sub sees strings on both platforms
            # Be safe and convert if neeeded
            if type(message.payload) != type(str()):
                message.payload = message.payload.decode("utf-8") 

            # Load message content
            j = json.loads(message.payload)
            uid = j['plant']['uid']
            humidity = j['plant']['humidity']

            temperature = None
            if 'temperature' in j['plant']:
                temperature = j['plant']['temperature']

            # Find the plant in the list
            # TODO look if plant is known
            # my_plant = None
            # for p in self._plants:
            #     if p.uid == uid and p.watering == plant.WateringMethod.conditional:
            #         my_plant = p
            #         break
            # STUB:
            class Plant:
                def __init__(self, uid):
                    self.uid = uid

            my_plant = Plant(uid)
            # END_STUB

            # Process event if the plant has conditional watering method
            if my_plant is not None:
                if temperature is not None and temperature >= 25:
                    # It's hot out there, the plant needs more water!
                    if humidity <= 60:
                        publish_watering_request(my_plant.uid)

                else:
                    if humidity <= 50:
                        publish_watering_request(my_plant.uid)

        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect('localhost')
        self.client.loop_forever()
