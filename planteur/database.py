"""This module provides a class that is able to store data in an SQLite3 database.

You can use SQLiteBrowser to visualize the data inside an SQLite3 file.
See http://sqlitebrowser.org/.
"""
import logging
import sqlite3
import threading

import paho.mqtt.client

import messaging


class DatabaseLogger:
    """An object able to log MQTT messages in a database.

    The database then contains an history of the data exchanged between the services.
    """

    def __init__(self, name):
        """Create a new instance.

        Tables are created if they don't exist.

        :param name: the name of the SQLite file
        :type name: str
        """
        self.conn = sqlite3.connect(name, check_same_thread=False)
        self.lock = threading.Lock()
        # It is not safe to share a connection between several threads: http://stackoverflow.com/a/22739924
        # This lock is here as a mutex
        self.client = paho.mqtt.client.Client()

        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plant(
                timestamp DATE,
                uid TEXT,
                humidity INTEGER,
                temperature INTEGER
            )
            ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ambient(
                timestamp DATE,
                uid TEXT,
                humidity INTEGER,
                temperature INTEGER
            )
            ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watering(
                timestamp DATE,
                uid TEXT
            )
            ''')

        self.conn.commit()

    def __del__(self):
        """Delete object and cleanup."""
        self.conn.close()

    def start(self):
        """Start the database logger thread."""
        name = '{} thread'.format(self.__class__.__name__)
        thread = threading.Thread(target=self._run, name=name)
        thread.start()

    def _run(self):
        """Receive and process MQTT messages."""

        # Define callbacks for MQTT
        def on_connect(client, userdata, flags, rc):
            logging.info('%s: connected with result %s', self.__class__.__name__, str(rc))
            client.subscribe('planteur/ambient')
            client.subscribe('planteur/plant')
            client.subscribe('planteur/watering')

        def on_message(client, userdata, message):
            logging.debug('%s: new message %s', self.__class__.__name__, message.payload)

            self.lock.acquire()
            cursor = self.conn.cursor()

            if message.topic == 'planteur/ambient':
                timestamp, uid, humidity, temperature = messaging.decode_ambient_message(message)

                cursor.execute('''
                INSERT INTO ambient(timestamp, uid, humidity, temperature) VALUES(?, ?, ?, ?)
                ''', (timestamp, uid, humidity, temperature))

            elif message.topic == 'planteur/plant':
                timestamp, uid, humidity, temperature = messaging.decode_plant_message(message)

                cursor.execute('''
                INSERT INTO plant(timestamp, uid, humidity, temperature) VALUES(?, ?, ?, ?)
                ''', (timestamp, uid, humidity, temperature))

            elif message.topic == 'planteur/watering':
                timestamp, uid = messaging.decode_watering_message(message)

                cursor.execute('''
                INSERT INTO watering(timestamp, uid) VALUES(?, ?)
                ''', (timestamp, uid))

            self.conn.commit()
            self.lock.release()

        # Set callbacks
        self.client.on_connect = on_connect
        self.client.on_message = on_message

        # Connect and wait for messages
        self.client.connect('localhost')  # FIXME extract hostname somewhere
        self.client.loop_forever()
