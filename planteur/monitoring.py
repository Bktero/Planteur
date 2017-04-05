"""This module provides classes for monitoring.

Monitoring gives the input data for the system by collecting the information
from the plants. Plants may periodically send data (eg: ZigBee, network) and it
may be necessary to ask them from time to time (eg: wired).
"""
import json
import logging
# import random
import serial
import socket
import threading
import time
import queue
from collections import namedtuple
from enum import Enum

__author__ = 'pgradot'

MonitoringEvent = namedtuple('MonitoringEvent',
                             ['timestamp', 'uid', 'humidity', 'temperature'])
"""When a monitoring event occurs, either because a plant has sent some data
or because Planteur has decided to read a sensor, a monitoring event is created. It
contains the time of generation, the UID of the plant, and the data from the
sensor.
"""


def create_monitoring_event(uid: str, humidity: int, temperature: float):
    """A factory method to create a monitoring event with the current time
    as the timestamp of the event.
    """
    return MonitoringEvent(time.time(), uid, humidity, temperature)


class MonitoringAggregator:
    """A MonitorAggregator processes events.

    It has an internal queue to safely receive events from other threads
    and process the events in its own thread."""

    def __init__(self, plants):
        self.listeners = list()
        self._plants = plants
        self._queue = queue.Queue()

    def post(self, event: MonitoringEvent):
        """Post an event that the aggregator will then consume."""
        self._queue.put(event)

    def start(self):
        """Start the aggregator's thread and start processing events."""
        aggregator_thread = threading.Thread(target=self._process_events,
                                             name=self.__class__.__name__ + 'thread')
        aggregator_thread.start()

    def _process_events(self):
        """Get events from the queue and process them.

        Basically, the aggregator drops events about unknown plants and
        broadcast other events to its listeners.
        """
        while True:
            # Retrieve event
            event = self._queue.get()
            logging.info('%s: processing event %s', self.__class__.__name__,
                         event)

            # Check if this plant is in the list
            known = False
            for plant_ in self._plants:
                if plant_.uid == event.uid:
                    known = True
                    break

            # Process or drop
            if known:
                for listener in self.listeners:
                    listener.process_event(event)
            else:
                logging.error('%s: unknown plant %s', self.__class__.__name__,
                              event.uid)

            # Release queue
            self._queue.task_done()


class StubWiredAdapter:
    """A StubWiredAdapter is a fake class to stub a plant with wired communication.
    Real wired adapters should read GPIO/ADC/etc to retrieve values from the sensors.
    """

    def __init__(self, aggregator: MonitoringAggregator, uid: str):
        """ Create a new adapter.
        :param uid: the UID of the plant
        """
        self.aggregator = aggregator
        self.uid = uid

    def start(self):
        """Start the thread for this stub adapter."""
        wired_thread = threading.Thread(target=self._poll_sensors,
                                        name="{}: {} thread".format(
                                            self.__class__.__name__, self.uid))
        wired_thread.start()

    def _poll_sensors(self):
        """Fake sensor polling."""
        i = 0
        while True:
            logging.info("%s: polling new value", self.__class__.__name__)
            # event = create_monitoring_event(self.uid, random.randint(0, 100), None)
            event = create_monitoring_event(self.uid, i, None)
            i += 1
            if i > 100:
                i = 0
            self.aggregator.post(event)
            time.sleep(1.2)


class NetworkAdapter:
    """A NetworkAdapter is able to receive monitoring data from the
    network.

    Plants that are connected to the local network send their data periodically.
    They use UDP packets. If a NetworkAdapter is listening on that port
    then it will receive the data, format in a common format and add then to a
    MonitoringAggregator.
    """

    def __init__(self, aggregator: MonitoringAggregator, ipaddr: str,
                 port: int):
        """Create a new NetworkAdapter.

        :param aggregator: the aggregator
        :param ipaddr: the IP address of the host
        :param port: the port to listen
        """
        self.aggregator = aggregator
        self.ipaddr = ipaddr
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        """Start the server thread."""
        server_thread = threading.Thread(target=self._run_server,
                                         name="{} on {}:{} server thread".format(
                                             self.__class__.__name__,
                                             self.ipaddr, self.port))
        server_thread.start()

    def _run_server(self):
        """Create UDP server, receive and process datagrams."""
        self.sock.bind((self.ipaddr, self.port))
        logging.info("%s: waiting for datagrams on %s:%d",
                     self.__class__.__name__, self.ipaddr, self.port)
        while True:
            message, address = self.sock.recvfrom(2048)
            # TODO adjust buffer size (for now, it is 2048 bytes)
            message_as_string = bytes.decode(message)
            logging.info("%s: received [%s] from %s", self.__class__.__name__,
                         message_as_string, address)
            json_dict = json.loads(message_as_string)
            event = create_monitoring_event(json_dict['plant']['uid'],
                                            json_dict['plant']['humidity'],
                                            json_dict['plant']['temperature'])
            self.aggregator.post(event)


class XBeeAdapter:
    """A XBeeAdapter is able to receive monitoring data from an XBee module
    accessible trough a serial port.

    Plants that are connected to the XBee wireless network send their data
    periodically. This adapter waits from their frame, format in a common format
     and add then to a MonitoringAggregator.
    """
    xbee_frame = namedtuple('frame', ['src', 'dest', 'payload'])

    class FrameType(Enum):
        plant = 1

    def __init__(self, aggregator: MonitoringAggregator, ser: serial,
                 uids: dict):
        """Create new XBeeAdapter.

        :param aggregator: the aggregator
        :param ser: the serial port to which the XBee module is connected
        :param uids: a dictionary with XBee ID as keys and plant UIDs as values
        """
        self.aggregator = aggregator
        self.ser = ser
        self.uids = uids

    def start(self):
        """Start the server thread."""
        server_thread = threading.Thread(target=self._run_server,
                                         name="{} on {} server thread".format(
                                             self.__class__.__name__,
                                             self.ser.name))
        server_thread.start()

    def _get_int(self):
        b = self.ser.read()
        i = int.from_bytes(b, byteorder='big')
        #print(i)
        return i

    def _get_frame(self):
        src = self._get_int()
        dest = self._get_int()
        length = self._get_int()
        payload = list()
        while length > 0:
            d = self._get_int()
            payload.append(d)
            length -= 1
        return self.xbee_frame(src, dest, payload)

    def _run_server(self):
        """Receive and process XBee frames."""
        logging.info("%s: waiting for frames on %s",
                     self.__class__.__name__, self.ser.name)
        while True:
            frame = self._get_frame()

            if frame.dest == 0 and frame.payload[0] == self.FrameType.plant.value: # Cannot compare directly an int and an enum
                logging.info("%s: received [%s]",
                             self.__class__.__name__, frame)
                uid = self.uids[str(frame.src)]
                humidity = frame.payload[1]
                temperature = frame.payload[2]
                event = create_monitoring_event(uid, humidity, temperature)
                self.aggregator.post(event)
            else:
                # The gateway is not the destination of this frame
                # or the type of frame is unknown
                logging.debug("%s: ignore frame %s",
                              self.__class__.__name__, frame)