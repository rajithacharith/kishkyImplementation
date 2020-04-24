import numpy as np
from SentenceLengthWeighting import getSentenceLengthWeightings
import os
import inputpaths

dim = 1024

pathA = inputpaths.enEmbeddingPath
pathB = inputpaths.siEmbeddingPath


def greedyMoversDistance(docA, docB, weightsA, weightsB):
    docVecA = getDocVec(docA, pathA)
    docVecB = getDocVec(docB, pathB)
    maxSortedVecs = getSortedDistances(docVecA, docVecB)
    minSortedVecs = np.flipud(maxSortedVecs)
    # print(minSortedVecs)

    distance = 0
    for sortedPair in minSortedVecs:
        weigVecA = weightsA[sortedPair["i"]]
        weigVecB = weightsB[sortedPair["j"]]
        flow = min(weigVecA, weigVecB)
        weightsA[sortedPair["i"]] = weigVecA - flow
        weightsB[sortedPair["j"]] = weigVecB - flow
        vecA = docVecA[sortedPair["i"]]
        vecB = docVecB[sortedPair["j"]]
        # only euclidean 100
        # distance = distance + np.linalg.norm(vecA - vecB) * flow
        # only cosine 112
        # distance = distance + (1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA)*np.linalg.norm(vecB))) * flow
        # cosine + euclidean 112
        distance = distance + ((1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA)*np.linalg.norm(vecB))) + np.linalg.norm(vecA - vecB)) * flow
        # unit euclidean and cosine 112
        # distance = distance + ((1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA)*np.linalg.norm(vecB))) + np.linalg.norm((vecA/np.linalg.norm(vecA)) - (vecB/np.linalg.norm(vecB)))) * flow

    # print("distance ", distance)
    return distance

def getSortedDistances(docVecA, docVecB):
    eucDistances = np.array([])
    for i in range(len(docVecA)):
        for j in range(len(docVecB)):
            eucDistances = np.append(eucDistances, [np.linalg.norm(docVecA[i] - docVecB[j])])
    sortedVecs = []
    for i in range(len(eucDistances)):
        maxi = eucDistances.argmax()
        sortedVecs.append({"dist": eucDistances[maxi], "i": maxi//len(docVecB), "j": maxi % len(docVecB)})
        eucDistances[maxi] = 0
    return sortedVecs

def getDocVec(doc, path):
    docVec = np.fromfile(path + doc, dtype = np.float32, count = -1)
    docVec.resize(docVec.shape[0] // dim, dim)
    return docVec

def temp(path1, path2):
    files1 = os.listdir(path1)
    files2 = os.listdir(path2)
    docDistances = []

    weightsA = []
    weightsB = []
    for file1 in files1:
        weightsA.append(getSentenceLengthWeightings(file1, "en"))
    for file2 in files2:
        weightsB.append(getSentenceLengthWeightings(file2, "si"))

    for i in range(len(files1)):
        if (i == 300):
            break
        print(i)
        tempDistances = []
        for j in range(len(files2)):
            weightA = weightsA[i].copy()
            weightB = weightsB[j].copy()
            tempDistances.append(greedyMoversDistance(files1[i], files2[j], weightA, weightB))
        docDistances.append([files1[i], files2[tempDistances.index(min(tempDistances))]])

    print(docDistances)
    count = 0
    for docDist in docDistances:
        if docDist[0] == docDist[1]:
            count = count + 1
    print("count  : " + str(count))

