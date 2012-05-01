__author__ = 'frieder'
import string
import numpy as np
import Loop
import pandas
import matplotlib.pyplot as plt
from scipy.stats import norm
import random


def convertToSax(phrase_length, symbol_count, d1):
    a = d1
    b = d1
    data = np.array([a, b])
    # Scale data to have a mean of 0 and a standard deviation of 1.
    data -= np.split(np.mean(data, axis=1), data.shape[0])
    data *= np.split(1.0 / data.std(axis=1), data.shape[0])
    # Calculate our breakpoint locations.
    breakpoints = norm.ppf(np.linspace(1. / symbol_count, 1 - 1. / symbol_count, symbol_count - 1))
    breakpoints = np.concatenate((breakpoints, np.array([np.Inf])))
    # Split the data into phrase_length pieces.
    data = np.array_split(data, phrase_length, axis=1)
    # Calculate the mean for each section.
    section_means = [np.mean(section, axis=1) for section in data]
    # Figure out which break each section is in based on the section_means and
    # calculated breakpoints.
    section_locations = [[np.where(breakpoints > axis_mean)[0][0]
                          for axis_mean in section_mean] for section_mean in section_means]
    section_locations = zip(*section_locations)
    # Convert the location into the corresponding letter.
    sax_phrases = [''.join([string.ascii_letters[ind] for ind in section_location])
                   for section_location in section_locations]
    return breakpoints, sax_phrases


def saxDistance(w1, w2, length, lookupTable, phrase_length, symbol_count):
    dist = 0
    for (l, k) in zip(w1, w2):
        dist += saxDistanceLetter(l, k, lookupTable, symbol_count)
    result = np.sqrt(dist) * np.sqrt(np.divide(length, phrase_length))
    return result


def saxDistanceLetter(w1, w2, lookupTable, symbol_count):
    n1 = ord(w1) - 97
    n2 = ord(w2) - 97

    if n1 > (symbol_count):
        raise Exception(" letter not in Dictionary " + w1)
    if n2 > (symbol_count):
        raise Exception(" letter not in Dictionary " + w2)
    return lookupTable[n1][n2]


def createLookup(symbol_count, breakpoints):
    return make_matrix(symbol_count, symbol_count, breakpoints)


def make_list(row, size, breakpoints):
    mylist = []
    for i in range(size):
        i = i + 1
        if abs(row - i) <= 1:
            mylist.append(0)
        else:
            v = breakpoints[(max(row, i) - 2)] - breakpoints[min(row, i) - 1]
            mylist.append(v)
    return mylist


def make_matrix(rows, cols, breakpoints):
    matrix = []
    for i in range(rows):
        i = i + 1
        matrix.append(make_list(i, cols, breakpoints))
    return matrix


def vocabToCoordinates(nd, phrase_length, phrases, points, symbol_count):
    retList = []
    p = phrases[0]
    newCutlines = points.tolist()

    max_value = points[symbol_count - 2] + ((points[symbol_count - 2] - points[symbol_count - 3]) * 2)
    # HERE IS SOMETHING WRONG // ONLY IN VISUALISATION
    min_value = points[0] - ((points[1] - points[0]) * 2)

    newCutlines.append(max_value)
    newCutlines.insert(0, min_value)
    co = nd.__len__()
    co1 = co / phrase_length

    for s in phrases[0]:
        for i in range(co1):
            retList.append(newCutlines[ord(s) - 97])
    return retList


def convertSaxBackToContinious(phrase_length, symbol_count, nd):
    points, phrases = convertToSax(phrase_length, symbol_count, nd)
    retList = vocabToCoordinates(nd, phrase_length, phrases, points, symbol_count)
    print phrases[0]
    return retList


def compareTwoRooms(id1, id2):
    symbol_count = 6
    phrase_length = 12
    samples = 30
    entries = Loop.getEntriesFromId(id1, samples, 1)
    nd = []
    for e in entries:
        nd.append(int(e["value"]))

    entries = Loop.getEntriesFromId(id2, samples, 1)
    nd2 = []
    for e in entries:
        nd2.append(int(e["value"]))

    sax1 = convertToSax(phrase_length, symbol_count, nd)
    sax2 = convertToSax(phrase_length, symbol_count, nd2)
    print sax1[1][0]
    print sax2[1][0]

    lookupTable = createLookup(symbol_count, sax1[0])
    print saxDistance(sax1[1][0], sax2[1][0], samples, lookupTable, phrase_length, symbol_count)

    pp = convertSaxBackToContinious(phrase_length, symbol_count, nd)
    pp1 = convertSaxBackToContinious(phrase_length, symbol_count, nd2)
    ts1 = pandas.Series(pp)
    ts2 = pandas.Series(pp1)
    ts1.plot(label="First Argument")
    ts2.plot(label="Second Argument")
    plt.legend(loc="upper left")
    plt.show()
def checkEqual3(lst):
    return lst[1:] == lst[:-1]

def check(id):
    entries = Loop.getEntriesFromId(id,10,1)
    nd = []
    for e in entries:
            nd.append((float(e["value"])))
    if checkEqual3(nd):
        nd[0] = (nd[0]+0.1)
    return nd

def test():
    symbol_count = 4
    phrase_length = 10
    #for n in Loop.getAvailableNodes():
    #    print n, type(n),Loop.getEntriesFromId(n).count()
    #    nd1 = check("49")
    #    nd2 = check("4AB6")
    #    print nd1,nd2
    nd= np.sin(np.linspace(0,2*np.pi,500))
        #nd = np.cos(np.linspace(0,2*np.pi, 500))

    pp = convertSaxBackToContinious(phrase_length, symbol_count, nd)

    breakpoints, sax_phrases = convertToSax(phrase_length, symbol_count,nd)
    print sax_phrases

    lookupTable = createLookup(symbol_count,breakpoints)
    #print saxDistance(sax_phrases[0],"bccccbbccccc",20)

    ts1 = pandas.Series(pp)
    ts2 = pandas.Series(nd)
    ts1.plot()
    ts2.plot()
    plt.show()

test()

