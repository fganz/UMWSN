__author__ = 'frieder'
from pymongo import Connection
connection = Connection()
db = connection.test_database
sensorEntries = db.entries
graphvalues = db.graphvalues
movementEntries = db.movement


def insertSensorEntry(data):
    sensorEntries.insert(data)

def getSensorEntries():
    return sensorEntries

