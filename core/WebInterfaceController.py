from core import SensorController, ProcessingController, DatabaseController, EventController

__author__ = 'frieder'

import cherrypy
import os.path
from mako.lookup import TemplateLookup


lookup  = TemplateLookup(directories='../')
current_dir = os.path.dirname(os.path.abspath(__file__))
selectionGlobal = "rolling_median"
timeframeGlobal = 2

class Data(object):
    def sensor(self,id):
        cherrypy.response.headers['content-type'] = 'text/csv'
        return SensorController.entryToCSVMA(id,selectionGlobal,timeframeGlobal)
    sensor.exposed = True

    def sensorSax(self,id):
        cherrypy.response.headers['content-type'] = 'text/csv'
        return ProcessingController.getSaxContinous(id,100)
    sensorSax.exposed = True

class RootHandler(object):
    data = Data()
    static = cherrypy.tools.staticdir.handler(
        section='static', root=os.path.dirname(current_dir), dir='static')

    def index(self):
        availableNodes = []
        n2 = []
        for n in SensorController.getAvailableNodes():
            availableNodes.append(str(n)+" in "+ EventController.mapSensorToRoom(n))

        print "Loop sensors",SensorController.getSensors()
        for n in SensorController.getSensors():
            print "FIDIRALALALA",n
            n2.append(n)

        return lookup.get_template("html/index.html").render(nod=n2,nodes = availableNodes,data=SensorController.getGraphValues(21),movementData=EventController.whereIsItMoving())
    index.exposed = True

    def sensorPage(self,selection="rolling_median",timeframe=2,id=21):
        global selectionGlobal
        global timeframeGlobal
        selectionGlobal = selection
        timeframeGlobal = timeframe
        return lookup.get_template("html/sensor.htm").render(data=SensorController.entryToCSVMA(id,selection,timeframe),thres=ProcessingController.getAvailableThresholds(),selection=selectionGlobal, timeframe = timeframeGlobal,id=id)
    sensorPage.exposed = True
    def deleteGraph(self,id):
        DatabaseController.graphvalues.remove({})
    deleteGraph.exposed = True

    def process(self,id,caption,x,y):
        #Loop.graphvalues.remove({})
        DatabaseController.graphvalues.insert({"_id":caption,"gID": id, "x": x, "y" : y})
    process.exposed = True

    def processRel(self,caption,From, To):
        #Loop.graphvalues.remove({})
        print From+" "+To
        DatabaseController.graphvalues.update({"_id":caption},{"$addToSet" : {"From": From, "To": To}})
    processRel.exposed = True


    def graph(self,id):
        return lookup.get_template("html/graph.html").render(data=SensorController.getGraphValues(id))
    graph.exposed = True



#Blocking
#for t in Loop.threads:
#    print t
#    cherrypy.engine.subscribe("stop",t.stop())
def start():
    cherrypy.quickstart(RootHandler())

