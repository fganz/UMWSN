from core import SensorController, EventController
from core.plugins.processing import SAX

__author__ = 'frieder'
def getSaxContinous(id, timeframe):
    nd = SensorController.getEntriesFromId(id,timeframe,1)
    nd2 = EventController.check(id,timeframe)
    out_str ="\"Date Time,SAX\\n\" +\n"
    if nd.count() >= timeframe:
        data = SAX.convertSaxBackToContinious(EventController.phrase_length, EventController.symbol_count, nd2)
        for (entry,sax) in zip(nd,data):
            #print entry,sax
            d = entry["date"]
            out_str += ""+str(d.year)+"/"+str(d.month)+"/"+str(d.day)+" "+str(d.hour)+":"+str(d.minute)+":"+str(d.second)+","+str(sax) + "\n"
    return out_str



def getAvailableThresholds():
    ret =[]
    ret.append("rolling_mean")
    ret.append("rolling_median")
    return ret