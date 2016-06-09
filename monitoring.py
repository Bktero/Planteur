"""This module provides classes for monitoring.

Monitoring gives the input data for the system by collecting the information
from the plants. Plants may periodically send data (eg: ZigBee, network) and it
may be necessary to ask them from time to time (eg: wired).
"""
import json
import logging
import random
import socket
import threading
import time
from queue import Queue
from collections import namedtuple

import database_storer

__author__ = 'pgradot'

MonitoringEvent = namedtuple('MonitoringEvent', ['timestamp', 'uid', 'humidity', 'temperature'])
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


class MonitoringAggregator(object):
    """A MonitorAggregator processes events.

    It has an internal queue.Queue to safely receive events from other threads
    and process the events in its own thread."""
    def __init__(self):
        self.queue = Queue()

    def add(self, event: MonitoringEvent):
        """Add a event that the aggregator will then consume."""
        self.queue.put(event)

    def start(self):
        """Start the aggregator's thread and start processing events."""
        aggregator_thread = threading.Thread(target=self._process_events, name=self.__class__.__name__ + 'thread')
        aggregator_thread.start()

    def _process_events(self):
        """Get events from the queue and process them.

        This is the internal function for the aggregator's thread."""
        db_storer = database_storer.DatabaseStorer('planteur.db')

        while True:
            event = self.queue.get()
            logging.info('%s: processing %s', self.__class__.__name__, event)
            db_storer.store_monitoring(event)
            self.queue.task_done()


class StubWiredAdapter(object):
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
        wired_thread = threading.Thread(target=self._poll_sensors, name="{}: {} thread".format(self.__class__.__name__, self.uid))
        wired_thread.start()

    def _poll_sensors(self):
        """Fake sensor polling."""
        while True:
            logging.info("%s: polling new value", self.__class__.__name__)
            event = create_monitoring_event(self.uid, random.randint(0, 100), None)
            self.aggregator.add(event)
            time.sleep(3)


class NetworkMonitoringAdapter(object):
    """A NetworkMonitoringAdapter is able to receive monitoring data from the
    network.

    Plants that are connected to the local network send their data periodically.
    They use UDP packets. If a NetworkMonitoringAdapter is listening of that port
    then it will receive the data, format in a common format and add then to a
    MonitoringAggregator.
    """

    def __init__(self, aggregator: MonitoringAggregator, ipaddr: str, port: int):
        """Create a new NetworkMonitoringAdapter.

        :param ipaddr: the IP address of the host
        :param port: the port to listen
        """
        self.aggregator = aggregator
        self.ipaddr = ipaddr
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        """Start the server thread."""
        server_thread = threading.Thread(target=self._run_server, name="{} on {}:{} server thread".format(self.__class__.__name__, self.ipaddr, self.port))
        server_thread.start()

    def _run_server(self):
        """Create UDP server, receive and process datagrams."""
        self.sock.bind((self.ipaddr, self.port))
        logging.info("%s: waiting for datagram on %s:%d", self.__class__.__name__, self.ipaddr, self.port)
        while True:
            message, address = self.sock.recvfrom(2048)
            # TODO adjust buffer size (for now, it is 2048 bytes)
            message_as_string = bytes.decode(message)
            logging.info("%s: received [%s] from %s", self.__class__.__name__, message_as_string, address)
            json_dict = json.loads(message_as_string)
            event = create_monitoring_event(json_dict['uid'], json_dict['humidity'], json_dict['temperature'])
            self.aggregator.add(event)
