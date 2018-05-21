"""This module provides classes for monitoring."""
import enum
import logging
import threading
from collections import namedtuple

import serial

import messaging


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

                messaging.publish_plant_message(uid, humidity=humidity, temperature=temperature)

            else:
                # The frame is rejected because of one of the following reasons:
                # - the gateway isn't its destination
                # - the source isn't known
                # - the frame type is not supported
                logging.warning('%s: frame ignored [%s]', self.__class__.__name__, frame)
