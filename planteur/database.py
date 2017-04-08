"""This module provides a class that is able to store data in an SQLite3
database.

You can use SQLiteBrowser to visualize the data inside an SQLite3 file.
See http://sqlitebrowser.org/.
"""
import sqlite3

__author__ = 'pgradot'


class DatabaseStorer:
    """An object able to store data in a database."""

    def __init__(self, name):
        """Create a new instance.

        Tables are created if they don't exist.

        :param name: the name of the SQLite file
        :type name: str
        """
        self.conn = sqlite3.connect(name, check_same_thread=False)

        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monitoring(
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

    def process_event(self, event):
        """ Store a monitoring event into the database.

        :param event: the monitoring event to store
        :type event: monitoring.MonitoringEvent
        """
        cursor = self.conn.cursor()

        cursor.execute('''
        INSERT INTO monitoring(timestamp, uid, humidity, temperature) VALUES(?, ?, ?, ?)
        ''', (event.timestamp, event.uid, event.humidity, event.temperature))

        self.conn.commit()

    def process_demand(self, demand):
        """Store a watering demand into the database.

        :param event: the watering demand to store
        :type event: watering.WateringDemand
        """
        cursor = self.conn.cursor()

        cursor.execute('''
        INSERT INTO watering(timestamp, uid) VALUES(?, ?)
        ''', (demand.timestamp, demand.uid))

        self.conn.commit()
