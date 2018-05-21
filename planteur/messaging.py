"""This modules helps to publish and receive messages from the MQTT server."""
import json
import logging
import time

import paho.mqtt.publish


def publish_plant_message(uid, humidity, temperature=None):
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
        logging.info('Publish plant message: %s', message)
        paho.mqtt.publish.single('planteur/plant', message)


def decode_plant_message(message):
    """Decode a message received from the 'planteur/plant' topic.

    :param message: a message from the MQTT server
    :return: uid, humidity, temperature (may be None)
    """
    if message.topic != 'planteur/plant':
        logging.error('Cannot decode plant message, topic is invalid: %s', message.topic)

        # Paho receives strings on Xubuntu but bytes on Raspbian
    # mosquitto_sub receives strings on both platforms
    # Be safe and convert if needed
    if type(message.payload) != type(str()):
        message.payload = message.payload.decode("utf-8")

    # Load message content
    j = json.loads(message.payload)
    uid = j['plant']['uid']
    humidity = j['plant']['humidity']

    temperature = None
    if 'temperature' in j['plant']:
        temperature = j['plant']['temperature']

    return uid, humidity, temperature


def publish_ambient_message(uid, humidity=None, temperature=None):
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
        logging.info('Publish ambient message: %s', message)
        paho.mqtt.publish.single('planteur/ambient', message)


def publish_watering_message(uid):
    """Publish a message to the 'planteur/watering' topic.

    :param uid: the UID of the plant
    """
    d = dict()
    d['watering'] = dict()
    d['watering']['uid'] = uid

    message = json.dumps(d)
    logging.info('Publish watering request: %s', message)
    paho.mqtt.publish.single('planteur/watering', message)
