__author__ = 'frieder'
import threading
import SensorController
import plugins.processing.SAX as SAX

symbol_count = 6
phrase_length = 10
frame_length = 10
class Watchdog(threading.Thread):
    def __init__(self, number_of_seconds_to_wait):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.number_of_seconds_to_wait = number_of_seconds_to_wait

    def run(self):
        while not self.event.is_set():
            for n in SensorController.getAvailableNodes():
                self.eventProcessing1()
            self.event.wait(self.number_of_seconds_to_wait)

    def stop(self):
        self.event.set()

    def eventProcessing1(self):

        for n in SensorController.getAvailableNodes():
            #print n,Loop.getEntriesFromId(n).count()
            if SensorController.getEntriesFromId(n).count() >= frame_length:

                data = check(n, frame_length)
                (points, cur) = SAX.convertToSax(phrase_length,symbol_count, data)
                #print n, cur[0]
                lookupTable = SAX.createLookup(symbol_count,points)
                #print SAX.convertSaxBackToContinious(phrase_length, symbol_count, data)
               # print SAX.saxDistance(cur[0],"aaaddddddd",frame_length,lookupTable,phrase_length,symbol_count),n
                if SAX.saxDistance(cur[0],"aaaddddddd",frame_length,lookupTable,phrase_length,symbol_count) < 2:
                 #   print "something happening at sensor "+str(n)
                    thereIsMovementIn(n)
                #print " "

def check(id, frames):

    entries = SensorController.getEntriesFromId(id,frames,1)
    nd = []

    for e in entries:
        if e["value"] is not None:
            nd.append((float(e["value"])))
            if nd[1:] == nd[:-1]:
                nd[0] = (nd[0]+0.1)
    return nd

def thereIsMovementIn(id):
    #movementEntries.insert({"Id":id,"date": datetime.datetime.utcnow()})
    print " to def"

def whereIsItMoving():

    res = []
    #for i in movementEntries.find({}).sort("$natural",-1).limit(5):
    #    print "movement in" + str(i["Id"])
    #    res.append("There is movement at "+str(mapSensorToRoom(i["Id"]))+" at "+i["date"].isoformat(" "))
    return res

def mapSensorToRoom(id):
    roomMap = {"21":"Desk Frieder","2":"Meeting Room E1","49": "Meeting Room E24", "116":"Meeting Room E6", "53F6":"SunSpot 1","4AB6":"SunSpot 2", "1":"Weather Guildford", "5":"Weather Santander"}
    return roomMap[id]