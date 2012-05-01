__author__ = 'frieder'
import threading
import datetime

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