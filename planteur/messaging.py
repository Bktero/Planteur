"""This modules helps to publish and receive messages from the MQTT server."""
import json
import logging
import time

import paho.mqtt.publish


# FIXME create constants for topics that other modules can use when they subscribe

def _sanitize(message):
    # Paho receives strings on Xubuntu but bytes on Raspbian
    # mosquitto_sub receives strings on both platforms
    # Be safe and convert if needed
    if isinstance(message.payload, bytes):
        # FIXME fix PEP8 warning about comparison
        message.payload = message.payload.decode("utf-8")


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
        d['plant']['timestamp'] = time.time()
        d['plant']['uid'] = uid
        d['plant']['humidity'] = humidity
        if temperature is not None:
            d['plant']['temperature'] = temperature

        message = json.dumps(d)
        logging.info('Publish plant message: %s', message)
        paho.mqtt.publish.single('planteur/plant', message)


def decode_plant_message(message):
    """Decode a message received from the 'planteur/plant' topic.

    :param message: a message from the MQTT server
    :return: timestamp, uid, humidity, temperature (may be None)
    """
    if message.topic != 'planteur/plant':
        logging.error('Cannot decode plant message, topic is invalid: %s', message.topic)

    _sanitize(message)

    # Load message content
    j = json.loads(message.payload)
    timestamp = j['plant']['timestamp']
    uid = j['plant']['uid']
    humidity = j['plant']['humidity']

    temperature = None
    if 'temperature' in j['plant']:
        temperature = j['plant']['temperature']

    return timestamp, uid, humidity, temperature


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
        d['ambient']['timestamp'] = time.time()
        d['ambient']['uid'] = uid
        if humidity is not None:
            d['ambient']['humidity'] = humidity
        if temperature is not None:
            d['ambient']['temperature'] = temperature

        message = json.dumps(d)
        logging.info('Publish ambient message: %s', message)
        paho.mqtt.publish.single('planteur/ambient', message)


def decode_ambient_message(message):
    """Decode a message received from the 'planteur/plant' topic.

    :param message: a message from the MQTT server
    :return: timestamp, uid, humidity, temperature (may be None)
    """
    if message.topic != 'planteur/ambient':
        logging.error('Cannot decode ambient message, topic is invalid: %s', message.topic)

    _sanitize(message)

    # Load message content
    j = json.loads(message.payload)
    timestamp = j['ambient']['timestamp']
    uid = j['ambient']['uid']

    humidity = None
    if 'humidity' in j['ambient']:
        humidity = j['ambient']['humidity']

    temperature = None
    if 'temperature' in j['ambient']:
        temperature = j['ambient']['temperature']

    return timestamp, uid, humidity, temperature


def publish_watering_message(uid):
    """Publish a message to the 'planteur/watering' topic.

    :param uid: the UID of the plant
    """
    d = dict()
    d['watering'] = dict()
    d['watering']['timestamp'] = time.time()
    d['watering']['uid'] = uid

    message = json.dumps(d)
    logging.info('Publish watering request: %s', message)
    paho.mqtt.publish.single('planteur/watering', message)


def decode_watering_message(message):
    """Decode a message received from the 'planteur/watering' topic.

    :param message: a message from the MQTT server
    :return: timestamp, uid
    """
    if message.topic != 'planteur/watering':
        logging.error('Cannot decode watering message, topic is invalid: %s', message.topic)

    _sanitize(message)

    # Load message content
    j = json.loads(message.payload)
    timestamp = j['watering']['timestamp']
    uid = j['watering']['uid']

    return timestamp, uid
