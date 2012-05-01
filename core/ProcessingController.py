__author__ = 'frieder'
def getSaxContinous(id, timeframe):
    nd = getEntriesFromId(id,timeframe,1)
    nd2 = Watchdog.check(id,timeframe)
    out_str ="\"Date Time,SAX\\n\" +\n"
    if nd.count() >= timeframe:
        data = SAX.convertSaxBackToContinious(Watchdog.phrase_length, Watchdog.symbol_count, nd2)
        for (entry,sax) in zip(nd,data):
            #print entry,sax
            d = entry["date"]
            out_str += ""+str(d.year)+"/"+str(d.month)+"/"+str(d.day)+" "+str(d.hour)+":"+str(d.minute)+":"+str(d.second)+","+str(sax) + "\n"
    return out_str

def entryToCSVMA(id,foo,timeframe):
    s =  getEntriesFromId(id,reverse=1)
    srs = Series(getDictFromId(id,reverse=1))
    # b = rolling_mean(srs, 50)


    b = eval(foo)(srs,int(timeframe))
    out_str ="\"Date Time,Temperature,MA\\n\" +\n"
    i = 0
    for entry in s:
        i+=1
        d = entry["date"]
        ma = b[d]
        if(i != s.count()):
            out_str += ""+str(d.year)+"/"+str(d.month)+"/"+str(d.day)+" "+str(d.hour)+":"+str(d.minute)+":"+str(d.second)+","+str(entry["value"])+","+str(ma) + "\n"
        else:
            out_str += ""+str(d.year)+"/"+str(d.month)+"/"+str(d.day)+" "+str(d.hour)+":"+str(d.minute)+":"+str(d.second)+","+str(entry["value"])+","+str(ma) +"\n"


    return out_str

def getAvailableThresholds():
    ret =[]
    ret.append("rolling_mean")
    ret.append("rolling_median")
    return ret