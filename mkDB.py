# A quick utility tool for creating the sqlite3 database

import sqlite3

conn = sqlite3.connect('peakFlowData.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS peakFlow
    (timestamp TEXT NOT NULL,
    reading TEXT NOT NULL)''')

conn.commit()
conn.close()
