__author__ = 'frieder'
def getAvailableNodes():
    return sensorEntries.distinct("Id")

def getLocationFromId(id):
    return sensorEntries.find({"Id":id}).distinct("Location")

def getEntriesFromId(id,limit=100,reverse=0):
    if reverse==1:
        return sensorEntries.find({"Id":id}).sort("$natural",-1).limit(limit)
    else:
        return sensorEntries.find({"Id":id}).limit(limit)

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
    s = graphvalues.find({"gID":str(id)})
    return s


def getDictFromId(id,reverse=0):
    s = getEntriesFromId(id,reverse=reverse)
    dict_ = {}
    for entry in s:
        d = entry["date"]
        v = entry["value"]
        dict_.setdefault(d,v)
    return dict_