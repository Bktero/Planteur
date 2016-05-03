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

__author__ = 'pgradot'


class StubWiredAdapter(object):
    """A StubWiredAdapter is a fake class to stub a plant with wired communication.
    Real wired adapters should read GPIO/ADC/etc to retrieve values from the sensors.
    """
    def __init__(self, uid: str):
        """ Create a new adapter.
        :param uid: the UID of the plant
        """
        self.uid = uid

    def start(self):
        """Start the thread for this stub adapter."""
        wired_thread = threading.Thread(target=self._poll_sensors, name="{}: {} thread".format(self.__class__.__name__, self.uid))
        wired_thread.start()

    def _poll_sensors(self):
        """Fake sensor polling."""
        while True:
            message = json.dumps({'uid': self.uid, 'humidity': random.randint(0, 100), 'temperature': random.randint(10, 30)})
            logging.info("%s: polled [%s]", self.__class__.__name__, message)
            time.sleep(3)


class NetworkMonitoringAdapter(object):
    """A NetworkMonitoringAdapter is able to receive monitoring data from the
    network.

    Plants that are connected to the local network send their data periodically.
    They use UDP packets. If a NetworkMonitoringAdapter is listening of that port
    then it will receive the data, format in a common format and add then to a
    MonitoringAggregator.
    """

    def __init__(self, ipaddr: str, port: int):
        """Create a new NetworkMonitoringAdapter.

        :param ipaddr: the IP address of the host
        :param port: the port to listen
        """
        self.ipaddr = ipaddr
        self.port = port

    def start(self):
        """Start the server thread."""
        server_thread = threading.Thread(target=self._run_server, name="{} on {}:{} server thread".format(self.__class__.__name__, self.ipaddr, self.port))
        server_thread.start()

    def _run_server(self):
        """Create UDP server, receive and process datagrams."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ipaddr, self.port))
        logging.info("%s: waiting for datagram on %s:%d", self.__class__.__name__, self.ipaddr, self.port)
        while True:
            message, address = self.sock.recvfrom(2048)
            # TODO adjust buffer size (for now, it is 2048 bytes)
            message_as_string = bytes.decode(message)
            logging.info("%s: received [%s] from %s", self.__class__.__name__, message_as_string, address)


