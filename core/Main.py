from core import Utils

__author__ = 'frieder'

from pymongo import Connection
from plugins.abstraction.GoogleWeather import WebNode
from plugins.abstraction.CCSRTestBed import TestBedNode
from plugins.abstraction.SunSpot import SunSpotNodeWrapper

connection = Connection()
db = connection.test_database
sensorEntries = db.entries
graphvalues = db.graphvalues
movementEntries = db.movement
sensors = []
threads = []


def loadSensors():
    print "Loading Sensors ..."
    SunSpotNodeWrapper()
    global sensors
    sensors = [TestBedNode("21",10,"PIR"),
               TestBedNode("2",10,"PIR"),
               TestBedNode("116",10,"PIR"),
               TestBedNode("49",10,"PIR"),
               WebNode("1",10,"Guildford"),
               WebNode("5",10,"Santander")]

    for s in sensors:
        print "starting",s
        t = Utils.Timer(s.getSamplingRate(),s)
        t.start()
        threads.append(t)

loadSensors()






#import matplotlib.pyplot as plt
#t1 = Series(getDictFromId(10))
#t2 = Series(getDictFromId(11))
#
#a1 = t1.plot()
#
#plt.show()
#print getSaxContinous("49",10)