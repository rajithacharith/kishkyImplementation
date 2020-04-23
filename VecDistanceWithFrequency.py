import numpy as np
import os
import json

dim = 1024

# result = 120

def calculateXLSMDForAllDocs(path1, path2):
    files1 = os.listdir(path1)
    files2 = os.listdir(path2)
    docDistances = []
    x = 0
    for file1 in files1:
        x = x + 1
        if (x == 500):
            break
        print(file1)
        print(x)
        tempDistances = []
        docVec1 = np.fromfile(path1 + file1, dtype=np.float32, count=-1)
        docVec1.resize(docVec1.shape[0] // dim, dim)
        for file2 in files2:
            docVec2 = np.fromfile(path2 + file2, dtype=np.float32, count=-1)
            docVec2.resize(docVec2.shape[0] // dim, dim)
            tempDistances.append(calculateXLSMD(docVec1, docVec2))
        docDistances.append([file1, files2[tempDistances.index(max(tempDistances))]])
    print(docDistances)
    count = 0
    for docDist in docDistances:
        if docDist[0] == docDist[1]:
            count = count + 1
    print("count : " + str(count))

def calculateXLSMD(docVecA, docVecB):
    totalDistances = []
    for vec1 in docVecA:
        allDistances = []
        relFrequencey1 = calculateRelativeSentenceFrequency(vec1, docVecA)
        for vec2 in docVecB:
            eucDis = np.linalg.norm(vec1 - vec2)
            allDistances.append(relFrequencey1 * calculateRelativeSentenceFrequency(vec2, docVecB) * eucDis)
        totalDistances.append(sum(allDistances))
    return np.exp(-sum(totalDistances))

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