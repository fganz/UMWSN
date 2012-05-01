from core.Node import Node
from xml.dom import minidom
import urllib
__author__ = 'frieder'

EXTERNAL_URL = 'http://131.227.92.112:8080/resteasy/restful-services/restservice/sensors/%s'
INTERNAL_URL = 'http://131.227.88.96:8080/resteasy/restful-services/restservice/sensors/%s'
NS = ''
class TestBedNode(Node):
    def __init__(self,id,samplingRate,sensor,location="Guildford",):
    #if sensor != ("PIR" or "light" or "temp"):
    #   raise Exception("sensor not available = "+sensor)
        self.samplingRate = samplingRate
        self.id = id
        self.sensor = sensor
        self.location = location
        self.type = "CCSR TestBed Source Node"
    def getSensorValue(self):
        url = EXTERNAL_URL % self.id
        dom = minidom.parse(urllib.urlopen(url))
        for n in dom.getElementsByTagName("reading"):
            return n.getElementsByTagName(self.sensor)[0].firstChild.data
            #            print n.getElementsByTagName("light")[0].firstChild.data
            #            print n.getElementsByTagName("temp")[0].firstChild.data
            #            print n.getElementsByTagName("timeStamp")[0].firstChild.data