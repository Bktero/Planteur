import random
import sqlite3
import time

DATABASE_NAME = 'planteur.db'

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS monitoring(
    timestamp DATE,
    uid TEXT,
    humidity INTEGER,
    temperature INTEGER
)
''')

# Add data
for _ in range(20):
    timestamp = time.time()
    uid = 'myplant#' + str(random.randint(0, 4))
    hum = random.randint(0, 100)
    temp = random.randint(10, 30)

    cursor.execute('''
    INSERT INTO monitoring(timestamp, uid, humidity, temperature) VALUES(?, ?, ?, ?)
    ''', (timestamp, uid, hum, temp))


# Commit and close database
conn.commit()
conn.close()