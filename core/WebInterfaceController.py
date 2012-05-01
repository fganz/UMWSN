__author__ = 'frieder'

import cherrypy
import os.path
import Loop
import time
from mako.lookup import TemplateLookup
import Watchdog

lookup  = TemplateLookup(directories='')
current_dir = os.path.dirname(os.path.abspath(__file__))
selectionGlobal = "rolling_median"
timeframeGlobal = 2

class Data(object):
    def sensor(self,id):
        cherrypy.response.headers['content-type'] = 'text/csv'
        return Loop.entryToCSVMA(id,selectionGlobal,timeframeGlobal)
    sensor.exposed = True

    def sensorSax(self,id):
        cherrypy.response.headers['content-type'] = 'text/csv'
        return Loop.getSaxContinous(id,100)
    sensorSax.exposed = True

class RootHandler(object):
    data = Data()
    static = cherrypy.tools.staticdir.handler(
        section='static', root=current_dir, dir='static')

    def index(self):
        availableNodes = []
        n2 = []
        for n in Loop.getAvailableNodes():
            availableNodes.append(str(n)+" in "+ Loop.mapSensorToRoom(n))

        print "Loop sensors",Loop.getSensors()
        for n in Loop.getSensors():
            print "FIDIRALALALA",n
            n2.append(n)

        return lookup.get_template("html/index.html").render(nod=n2,nodes = availableNodes,data=Loop.getGraphValues(21),movementData=Loop.whereIsItMoving())
    index.exposed = True
    def deleteGraph(self,id):
        Loop.graphvalues.remove({})
    deleteGraph.exposed = True

    def process(self,id,caption,x,y):
        #Loop.graphvalues.remove({})
        Loop.graphvalues.insert({"_id":caption,"gID": id, "x": x, "y" : y})
    process.exposed = True

    def processRel(self,caption,From, To):
        #Loop.graphvalues.remove({})
        print From+" "+To
        Loop.graphvalues.update({"_id":caption},{"$addToSet" : {"From": From, "To": To}})
    processRel.exposed = True


    def graph(self,id):
        return lookup.get_template("html/graph.html").render(data=Loop.getGraphValues(id))
    graph.exposed = True


Loop.start()
Watchdog.Watchdog(1).start()
#Blocking
#for t in Loop.threads:
#    print t
#    cherrypy.engine.subscribe("stop",t.stop())
cherrypy.quickstart(RootHandler())

