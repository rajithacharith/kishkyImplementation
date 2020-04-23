import numpy as np
import os
import json

dim = 1024

# result = 153

def calculateXLSMDForAllDocs(path1, path2):
    files1 = os.listdir(path1)
    files2 = os.listdir(path2)
    docDistances = []
    x = 0
    for file1 in files1:
        x = x + 1
        if (x == 30):
            break
        print(file1)
        print(x)
        tempDistances = []
        docVec1 = np.fromfile(path1 + file1, dtype=np.float32, count=-1)
        docVec1.resize(docVec1.shape[0] // dim, dim)
        for file2 in files2:
            docVec2 = np.fromfile(path2 + file2, dtype=np.float32, count=-1)
            docVec2.resize(docVec2.shape[0] // dim, dim)
            tempDistances.append(calculateXLSMD(docVec1, docVec2, file1, file2))
        docDistances.append([file1, files2[tempDistances.index(max(tempDistances))]])
        # if(x == 30):
        #     break
    print(docDistances)
    count = 0
    for docDist in docDistances:
        if docDist[0] == docDist[1]:
            count = count + 1
    print("count  : " + str(count))

def calculateXLSMD(docVecA, docVecB, file1, file2):
    totalDistances = []
    x = 0
    for vec1 in docVecA:
        allDistances = []
        tokenCount1 = getTokenCount(file1, x, "en", vec1, docVecA)
        x = x + 1
        # if tokenCount1 == 0:
        #     print(0)
        #     continue
        weight1 = tokenCount1
        y = 0
        for vec2 in docVecB:
            eucDis = np.linalg.norm(vec1 - vec2)
            tokenCount2 = getTokenCount(file2, y, "si", vec2, docVecB)
            y = y + 1
            # if tokenCount2 == 0:
            #     print(0)
            #     continue
            allDistances.append(weight1 * tokenCount2 * eucDis)
        totalDistances.append(sum(allDistances))
    return np.exp(-sum(totalDistances))

def getTokenCount(filename, sentence, lang, vec, docVec):
    txtFile = open("/home/dilan/Private/Projects/FYP/Data-Formatted/" + lang + "/" + filename.replace("raw", "txt"), "r")
    lines = txtFile.readlines()
    totTokenCount = 0
    x = 0
    tokenCount = 0
    for line in lines:
        totTokenCount = totTokenCount + len(line.split())
        if x == sentence:
            # print(line)
            # print(line.split())
            tokenCount = len(line.split())
        x = x + 1
    #print(tokenCount)
    #print(totTokenCount)
    # if tokenCount == 1:
    #     print(0)
    #     return 0
    sentCount = 0
    for tempVec in docVec:
        if np.linalg.norm(tempVec - vec) == 0:
            sentCount = sentCount + 1
    return ((tokenCount * sentCount)/(totTokenCount))

def calculateRelativeSentenceFrequency(vec, docVec):
    count = 0
    for tempVec in docVec:
        if np.linalg.norm(tempVec - vec) == 0:
            count = count + 1
    # print(count)
    if (count == 0):
        print(count)
        return 1/len(docVec)
    return count/len(docVec)

calculateXLSMDForAllDocs("/home/dilan/Private/Projects/FYP/Embeddings/en/", "/home/dilan/Private/Projects/FYP/Embeddings/si/")
#print(getTokenCount("101800.raw", 1, "en"))