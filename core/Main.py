__author__ = 'frieder'
import Node
import threading
import random
import pymongo
from pymongo import Connection
from pandas import *
import datetime
import Watchdog
import SAX

connection = Connection()
db = connection.test_database
sensorEntries = db.entries
graphvalues = db.graphvalues
movementEntries = db.movement
sensors = []
threads = []

class Timer(threading.Thread):
    def __init__(self, number_of_seconds_to_wait, foo):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.foo = foo
        self.number_of_seconds_to_wait = number_of_seconds_to_wait
    def run(self):
        while not self.event.is_set():
            sensorEntry = {"Id": self.foo.getId(),"Location": self.foo.getLocation(),"value":self.foo.getSensorValue(),"date": datetime.datetime.utcnow()}

            sensorEntries.insert(sensorEntry)
            #print sensorEntry
            self.event.wait(self.number_of_seconds_to_wait)
    def stop(self):
        self.event.set()

def printOut(valuse):
    print valuse()
    return valuse

def getAvailableNodes():
    return sensorEntries.distinct("Id")

def getLocationFromId(id):
    return sensorEntries.find({"Id":id}).distinct("Location")

def getEntriesFromId(id,limit=100,reverse=0):
    if reverse==1:
        return sensorEntries.find({"Id":id}).sort("$natural",-1).limit(limit)
    else:
        return sensorEntries.find({"Id":id}).limit(limit)

def start():
    print "Starting sensing Loop"
    Node.SunSpotNodeWrapper()
    #sensors = [Node.Node(10,5), Node.Node(11,10)]
   # sensors = [Node.TestBedNode(21,10,"light")]
    global sensors
    sensors = [Node.TestBedNode("21",10,"PIR"),
               Node.TestBedNode("2",10,"PIR"),
               Node.TestBedNode("116",10,"PIR"),
               Node.TestBedNode("49",10,"PIR"),
               Node.WebNode("1",10,"Guildford"),
 #            Node.WebNode(2,"Karlsruhe",random.randint(1,10)),
  #           Node.WebNode(3,"Honolulu",random.randint(1,10)),
   #         Node.WebNode(4,"Berlin",random.randint(1,10)),
            Node.WebNode("5",10,"Santander")]

    for s in sensors:
        print "starting",s
        t = Timer(s.getSamplingRate(),s)
        t.start()
        threads.append(t)
def getSensors():
    global sensors
    return sensors

def entryToCSV(id):
    s =  getEntriesFromId(id)
    out_str ="\"Date Time,Temperature\\n\" +\n"
    i = 0
    for entry in s:
        i+=1
        d = entry["date"]
        if(i != s.count()):
            out_str += ""+str(d.year)+"/"+str(d.month)+"/"+str(d.day)+" "+str(d.hour)+":"+str(d.minute)+":"+str(d.second)+","+str(entry["value"]) + "\n"
        else:
            out_str += ""+str(d.year)+"/"+str(d.month)+"/"+str(d.day)+" "+str(d.hour)+":"+str(d.minute)+":"+str(d.second)+","+str(entry["value"]) +"\n"
    return out_str

def getGraphValues(id):
    s = graphvalues.find({"gID":str(id)})
    return s


def getDictFromId(id,reverse=0):
    s = getEntriesFromId(id,reverse=reverse)
    dict_ = {}
    for entry in s:
        d = entry["date"]
        v = entry["value"]
        dict_.setdefault(d,v)
    return dict_

def getSaxContinous(id, timeframe):
    nd = getEntriesFromId(id,timeframe,1)
    nd2 = Watchdog.check(id,timeframe)
    out_str ="\"Date Time,SAX\\n\" +\n"
    if nd.count() >= timeframe:
        data = SAX.convertSaxBackToContinious(Watchdog.phrase_length, Watchdog.symbol_count, nd2)
        for (entry,sax) in zip(nd,data):
            #print entry,sax
            d = entry["date"]
            out_str += ""+str(d.year)+"/"+str(d.month)+"/"+str(d.day)+" "+str(d.hour)+":"+str(d.minute)+":"+str(d.second)+","+str(sax) + "\n"
    return out_str

def entryToCSVMA(id,foo,timeframe):
    s =  getEntriesFromId(id,reverse=1)
    srs = Series(getDictFromId(id,reverse=1))
   # b = rolling_mean(srs, 50)


    b = eval(foo)(srs,int(timeframe))
    out_str ="\"Date Time,Temperature,MA\\n\" +\n"
    i = 0
    for entry in s:
        i+=1
        d = entry["date"]
        ma = b[d]
        if(i != s.count()):
            out_str += ""+str(d.year)+"/"+str(d.month)+"/"+str(d.day)+" "+str(d.hour)+":"+str(d.minute)+":"+str(d.second)+","+str(entry["value"])+","+str(ma) + "\n"
        else:
            out_str += ""+str(d.year)+"/"+str(d.month)+"/"+str(d.day)+" "+str(d.hour)+":"+str(d.minute)+":"+str(d.second)+","+str(entry["value"])+","+str(ma) +"\n"


    return out_str

def getAvailableThresholds():
    ret =[]
    ret.append("rolling_mean")
    ret.append("rolling_median")
    return ret

def thereIsMovementIn(id):
    movementEntries.insert({"Id":id,"date": datetime.datetime.utcnow()})

def whereIsItMoving():

    res = []
    for i in movementEntries.find({}).sort("$natural",-1).limit(5):
        print "movement in" + str(i["Id"])
        res.append("There is movement at "+str(mapSensorToRoom(i["Id"]))+" at "+i["date"].isoformat(" "))
    return res

def mapSensorToRoom(id):
    roomMap = {"21":"Desk Frieder","2":"Meeting Room E1","49": "Meeting Room E24", "116":"Meeting Room E6", "53F6":"SunSpot 1","4AB6":"SunSpot 2", "1":"Weather Guildford", "5":"Weather Santander"}
    return roomMap[id]
#import matplotlib.pyplot as plt
#t1 = Series(getDictFromId(10))
#t2 = Series(getDictFromId(11))
#
#a1 = t1.plot()
#
#plt.show()
#print getSaxContinous("49",10)