__author__ = 'frieder'


import random
import Loop



class Node:
    def __init__(self,id,samplingRate,location = "Santander",):
        self.samplingRate = samplingRate
        self.id = id
        self.location = location
        self.type = "Random Generator Source Node"

    def getSensorValue(self):
        return random.randint(1,10)

    def getSamplingRate(self):
        return self.samplingRate

    def getId(self):
        return self.id

    def getLocation(self):
        return self.location

    def getDescription(self):
        return Loop.mapSensorToRoom(self.id)

    def getPluginType(self):
        return self.type


