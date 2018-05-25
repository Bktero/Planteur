"""This modules provides classes for watering."""
import logging
import threading

import paho.mqtt.client

import messaging
import plant


class Sprinkler:
    def __init__(self, plants):
        self.client = paho.mqtt.client.Client()
        self.plants = plants

    def start(self):
        """Start the sprinkler thread."""
        name = '{} thread'.format(self.__class__.__name__)
        thread = threading.Thread(target=self._run, name=name)
        thread.start()

    def _run(self):
        """Receive and process MQTT messages."""

        # Define callbacks for MQTT
        def on_connect(client, userdata, flags, rc):
            logging.info('%s: connected with result %s', self.__class__.__name__, str(rc))
            client.subscribe('planteur/plant')

        def on_message(client, userdata, message):
            logging.debug('%s: new message %s', self.__class__.__name__, message.payload)

            timestamp, uid, humidity, temperature = messaging.decode_plant_message(message)

            # Find the plant in the list
            the_plant = None
            for p in self.plants:
                if p.uid == uid:
                    the_plant = p
                    break

            # Process event if the plant has conditional watering method
            if the_plant is not None and the_plant.watering == plant.WateringMethod.conditional:
                if temperature is not None and temperature >= 25:
                    # It's hot out there, the plant needs more water!
                    if humidity <= 60:
                        messaging.publish_watering_message(the_plant.uid)

                else:
                    if humidity <= 50:
                        messaging.publish_watering_message(the_plant.uid)
            else:
                logging.debug('%s: ignore message because %s is not watered conditionally', self.__class__.__name__,
                              the_plant.uid)

        # Set callbacks
        self.client.on_connect = on_connect
        self.client.on_message = on_message

        # Connect and wait for messages
        self.client.connect('localhost')
        self.client.loop_forever()
