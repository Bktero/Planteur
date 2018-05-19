"""This module provides classes for monitoring."""
# import random
import enum
import json
import logging
import threading
import time
from collections import namedtuple

import paho.mqtt.publish
import serial


def publish_plant_event(uid, humidity, temperature=None):
    """ Publish a message to the 'planteur/plant' topic.

    :param uid: the UID of the plant
    :param humidity: the humidity (mandatory)
    :param temperature: the temperature (optional)
    """
    if humidity is None:
        logging.warning('Plant message cannot be published because humidity is not defined')

    else:
        d = dict()
        d['plant'] = dict()
        d['plant']['uid'] = uid
        d['plant']['timestamp'] = time.time()
        d['plant']['humidity'] = humidity
        if temperature is not None:
            d['plant']['temperature'] = temperature

        message = json.dumps(d)
        logging.info('Publish plant event: %s', message)
        paho.mqtt.publish.single('planteur/plant', message)


def publish_ambient_event(uid, humidity=None, temperature=None):
    """ Publish a message to the 'planteur/ambient' topic.

    At least humidity or temperature should be provided. Otherwise, message is discarded.

    :param uid: the UID of the place
    :param humidity: the humidity (optional)
    :param temperature: the temperature (optional)
    """
    if (humidity is None) and (temperature is None):
        logging.warning('Ambient message cannot be published because neither humidity nor temperature is defined')

    else:
        d = dict()
        d['ambient'] = dict()
        d['ambient']['uid'] = uid
        d['ambient']['timestamp'] = time.time()
        if humidity is not None:
            d['ambient']['humidity'] = humidity
        if temperature is not None:
            d['ambient']['temperature'] = temperature

        message = json.dumps(d)
        logging.info('Publish ambient event: %s', message)
        paho.mqtt.publish.single('planteur/ambient', message)


class SerialMonitor:
    """A SerialMonitor is monitor from a serial port.

    It reads the serial port to extract frames that are then published to the MQTT server.
    """
    # TODO document serial frame format
    frame = namedtuple('frame', ['dest', 'src', 'type', 'payload'])

    class FrameType(enum.Enum):
        plant = 1

    def __init__(self, serial_port: serial, uid_dict: dict):
        """Create new instance.

        :param serial_port: the serial port to read from
        :param uid_dict: a dictionary with Serial ID as keys (int) and plant UIDs (str) as values
        """
        self.serial_port = serial_port
        self.uid_dict = uid_dict

    def start(self):
        """Start the serial monitor thread."""
        name = '{} (port = {}) thread'.format(self.__class__.__name__, self.serial_port.name)
        thread = threading.Thread(target=self._run, name=name)
        thread.start()

    def _get_int(self):
        """Get the next byte from the serial port as an int."""
        b = self.serial_port.read()
        i = int.from_bytes(b, byteorder='big')
        # print(i)
        return i

    def _get_next_frame(self):
        """Get the next frame from the serial port."""
        dest = self._get_int()
        src = self._get_int()
        type = self._get_int()

        length = self._get_int()
        payload = list()
        while length > 0:
            d = self._get_int()
            payload.append(d)
            length -= 1

        return self.frame(dest, src, type, payload)

    def _run(self):
        """Receive and process frames."""
        logging.info('%s: waiting for frames on %s', self.__class__.__name__, self.serial_port.name)

        while True:
            frame = self._get_next_frame()

            if frame.dest == 0 and frame.src in self.uid_dict and frame.type == self.FrameType.plant.value:
                # This frame contains a plant event
                logging.debug('%s: frame received [%s]', self.__class__.__name__, frame)

                uid = self.uid_dict[frame.src]
                humidity = frame.payload[0]
                temperature = frame.payload[1]

                publish_plant_event(uid, humidity=humidity, temperature=temperature)

            else:
                # The frame is rejected because of one of the following reasons:
                # - the gateway isn't its destination
                # - the source isn't known
                # - the frame type is not supported
                logging.warning('%s: frame ignored [%s]', self.__class__.__name__, frame)
