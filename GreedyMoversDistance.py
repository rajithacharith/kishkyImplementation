import numpy as np
from SentenceLengthWeighting import getSentenceLengthWeightings
import os
import inputpaths

dim = 1024

def greedyMoversDistance(docA, docB, weightsA, weightsB, embedpathA, embedpathB):
    docVecA = getDocVec(docA, embedpathA)
    docVecB = getDocVec(docB, embedpathB)
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
        # only euclidean
        # distance = distance + np.linalg.norm(vecA - vecB) * flow
        # only cosine
        # distance = distance + (1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA)*np.linalg.norm(vecB))) * flow
        # cosine + euclidean
        distance = distance + ((1 - np.dot(vecA, vecB)/(np.linalg.norm(vecA)*np.linalg.norm(vecB))) + np.linalg.norm(vecA - vecB)) * flow
        # unit euclidean and cosine
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


