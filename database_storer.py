"""This module provides a class that is able to store data in an SQLite3
database.

To visualize the data inside an QSLite3 file, you can use SQLiteBrower. See
http://sqlitebrowser.org/.
"""
import sqlite3

import monitoring

__author__ = 'pgradot'


class DatabaseStorer:
    """An object able to store data in a database."""
    def __init__(self, name:str):
        """Create a new instance.

        :param name: the name of the SQLite file
        """
        self.conn = sqlite3.connect(name)

        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monitoring(
                timestamp DATE,
                uid TEXT,
                humidity INTEGER,
                temperature INTEGER
            )
            ''')
        self.conn.commit()

    def __del__(self):
        """Delete object and cleanup."""
        self.conn.close()

    def store_monitoring(self, event):
        """ Store a monitoring event in the database.

        :param event: the monitoring event to store"""
        cursor = self.conn.cursor()

        cursor.execute('''
        INSERT INTO monitoring(timestamp, uid, humidity, temperature) VALUES(?, ?, ?, ?)
        ''', (event.timestamp, event.uid, event.humidity, event.temperature))

        self.conn.commit()