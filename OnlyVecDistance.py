import numpy as np
import os
import json

dim = 1024

def calculateXLSMDForAllDocs(path1, path2):
    files1 = os.listdir(path1)
    files2 = os.listdir(path2)
    docDistances = []
    for file1 in files1:
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
    print("count  : " + str(count))

def calculateXLSMD(docVecA, docVecB):
    totalDistances = []
    for vec1 in docVecA:
        allDistances = []
        for vec2 in docVecB:
            eucDis = np.linalg.norm(vec1 - vec2)
            allDistances.append(eucDis)
        totalDistances.append(min(allDistances))
    return np.exp(-sum(totalDistances))

calculateXLSMDForAllDocs("/home/dilan/Private/Projects/FYP/Embeddings/gossiplanka/en/", "/home/dilan/Private/Projects/FYP/Embeddings/gossiplanka/si/")