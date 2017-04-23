import json
import random
import socket
import time
import sys


class NetworkPlant(object):
    """A stub plant that communicate thought network with UPD."""

    def __init__(self, uid: str):
        self.uid = uid
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, humidity: int, temperature: int):
        """ Send a UDP datagram with generate stub data.
        :param humidity: the humidity
        :param temperature: the temperature
        """
        message = json.dumps({'plant':
            {
                'uid': self.uid,
                'humidity': humidity,
                'temperature': temperature
            }
        })

        message_as_bytes = message.encode()
        self.sock.sendto(message_as_bytes, (UDP_IPADDR, UDP_PORT))


if __name__ == '__main__':
    print('network_plants starts')

    # Address and port of the Planteur
    UDP_IPADDR = 'localhost'
    UDP_PORT = 14246

    # Plants connected to the network
    cactus = NetworkPlant('pgt_cactus_network')
    ficus = NetworkPlant('pgt_ficus_network')
    tomatoes = NetworkPlant('pgt_tomatoes_network')
    plants = [tomatoes, ficus, cactus]

    if sys.argv[1] == 'functional':
        print('functional tests')

        # Cactus = no watering
        # It won't generate watering demands, only monitoring events
        cactus.send(humidity=70, temperature=22)
        cactus.send(humidity=30, temperature=22)
        cactus.send(humidity=52, temperature=30)

        # Ficus = planned
        # It won't generate watering demands, only monitoring events
        ficus.send(humidity=70, temperature=22)
        ficus.send(humidity=30, temperature=22)
        ficus.send(humidity=52, temperature=30)

        # Tomatoes = conditional
        # It will generate both monitoring events and watering demands
        tomatoes.send(humidity=70, temperature=22)
        tomatoes.send(humidity=30, temperature=22)
        tomatoes.send(humidity=52, temperature=30)

    elif sys.argv[1] == 'intense':
        print('intense tests')
        humidity = 0
        while humidity < 100:
            cactus.send(humidity=humidity, temperature=25)
            tomatoes.send(humidity=humidity, temperature=20)
            humidity += 1

    else:
        print('This script expect either "functional" or "intense" as its single parameter')


