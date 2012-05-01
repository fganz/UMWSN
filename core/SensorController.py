from core import DatabaseController, Utils
from pandas import Series,rolling_mean,rolling_median


__author__ = 'frieder'


sensors = []
threads = []


def start():
    from core.plugins.abstraction.CCSRTestBed import TestBedNode
    from core.plugins.abstraction.GoogleWeather import WebNode
    from core.plugins.abstraction.SunSpot import SunSpotNodeWrapper
    from core.Node import Node
    print "Loading Sensors ..."
    #SunSpotNodeWrapper()
    global sensors
    sensors = [TestBedNode("21",10,"PIR"),
               TestBedNode("2",10,"PIR"),
               TestBedNode("116",10,"PIR"),
               TestBedNode("49",10,"PIR"),
               WebNode("1",10,"Guildford"),
               WebNode("5",10,"Santander"),
               Node("1000",10,"Saarbruecken")]

    for s in sensors:
        print "starting",s
        t = Utils.Timer(s.getSamplingRate(),s)
        t.start()
        threads.append(t)

def getAvailableNodes():
    return DatabaseController.getSensorEntries().distinct("Id")

def getLocationFromId(id):
    return DatabaseController.getSensorEntries().find({"Id":id}).distinct("Location")

def getEntriesFromId(id,limit=100,reverse=0):
    if reverse==1:
        return DatabaseController.getSensorEntries().find({"Id":id}).sort("$natural",-1).limit(limit)
    else:
        return DatabaseController.getSensorEntries().find({"Id":id}).limit(limit)

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
    s = DatabaseController.graphvalues.find({"gID":str(id)})
    return s


def getDictFromId(id,reverse=0):
    s = getEntriesFromId(id,reverse=reverse)
    dict_ = {}
    for entry in s:
        d = entry["date"]
        v = entry["value"]
        dict_.setdefault(d,v)
    return dict_

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