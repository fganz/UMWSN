from core.Node import Node

__author__ = 'frieder'
import pywapi

class WebNode(Node):
    def __init__(self,id,samplingRate,location="Guildford"):
        self.samplingRate = samplingRate
        self.id = id
        self.location = location
        self.type = "RestFul Access Source Node"
    def getSensorValue(self):
        google_result = pywapi.get_weather_from_google(self.location)
        return google_result['current_conditions']['temp_c']

    def getLocation(self):
        return self.location