import numpy as np
import inputpaths

def getSentenceLengthWeightings(datapath, fileName):
    docFile = open(datapath + fileName.replace("raw", "txt"))
    sentenceCounts = getSentenceCounts(docFile)
    weightings = []
    total = getTotalTokenCount(sentenceCounts)
    for sentenceCount in sentenceCounts:
        weightings.append(sentenceCount/total)
    return weightings

def getSentenceCounts(docFile):
    lines = docFile.readlines()
    counts = []
    for line in lines:
        count = 0
        for alllines in lines:
            if line == alllines:
                count = count + 1
        counts.append(count * len(line.split()))
    return counts

def getTotalTokenCount(counts):
    total = 0
    for count in counts:
        total = total + count
    return total