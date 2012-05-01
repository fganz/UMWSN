from core import Utils, SensorController
from core.Node import Node

__author__ = 'frieder'
import socket
import sys
from threading import Thread


class SunSpotNodeWrapper():
    spotNodes = []
    def __init__(self,sock=None):
        print "SunSpot Node Init"
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

        try:
            self.connect("localhost",4444)
            t =  Thread(target=self.read)
            t.start()
            #t.join()
        except Exception, errtxt:
            print errtxt

    def connect(self, host, port):
        try:
            self.sock.connect((host,port))
        except socket.error:
            print "Connection refused could not connect to SunSpot Wrapper"

    def read(self):
        file = self.sock.makefile()
        while 1:
            line = file.readline()
            if not line: break
            if "who:" in line:
                ieee = line.split(":")[1]
                ieeeShort = ieee.split(".")[3].strip("\r\n")
                n = SunSpotNode(ieeeShort)

                if n not in self.spotNodes:
                    self.spotNodes.append(n)
                    Utils.Timer(1,n).start()
                    SensorController.sensors.append(n)

            if line.startswith("V"):
                splitted =line.split(":")
                ieeeShort = splitted[1].split(".")[3].strip("\r\n")
                xValue = splitted[2]
                for n in self.spotNodes:
                    if n.getId() == ieeeShort:
                        n.value = xValue



    #We have to use the newline character as the Java Server uses Readline
    def sendCmd(self, cmd):
        r = self.sock.send(cmd+"\n")
        print r

    def getNodes(self):
        return self.spotNodes

class SunSpotNode(Node):
    def __init__(self,id,location="Santander",):
        self.value = 0.0
        self.id = id
        self.location=location
        self.type = "Oracle SunSpot Source Node"
    def getSensorValue(self):
        return self.value
    def __cmp__(self, other):
        if self.getId() == other.getId():
            return 0
        else:
            return -1



