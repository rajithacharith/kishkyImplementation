import os
from GreedyMoversDistance import greedyMoversDistance
from SentenceLengthWeighting import getSentenceLengthWeightings
from MergeSort import mergeSort
from CompetitiveMatching import competitiveMatching
from IDFWeighting import getIDFWeightingsForFile, getSentenceDict
import numpy as np
import inputpaths

pathA = inputpaths.enEmbeddingPath
pathB = inputpaths.siEmbeddingPath

def main():
    # sentenceLengthAlignment()
    # IDFAlignment()
    SLIDFAlignment()


def sentenceLengthAlignment(): # hiru -  325/500 # gosssip - 296/300 # wsws - 497/500 # army - 523/535 # itn - 41/51
    files1 = os.listdir(pathA)
    files2 = os.listdir(pathB)
    docDistances = []

    weightsA = []
    weightsB = []
    for file1 in files1:
        weightsA.append(normalizeDocumentMass(getSentenceLengthWeightings(file1, "en")))
    for file2 in files2:
        weightsB.append(normalizeDocumentMass(getSentenceLengthWeightings(file2, "si")))
    tempDistances = []
    for i in range(len(files1)):
        # print(i)
        # if i == 500:
        #     print("breaking")
        #     break
        
        for j in range(len(files2)):
            # if j == 500:
            #     print("breaking")
            #     break
            weightA = weightsA[i].copy()
            weightB = weightsB[j].copy()
            tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB)})

    mergeSort(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    count = 0
    for matchedPair in matchedPairs:
        if matchedPair["a"] == matchedPair["b"]:
            count = count + 1
    print(matchedPairs)
    print("sentence length count  : " + str(count))

def IDFAlignment(): # hiru - 281/500 # gosssip - 287/300 # army - 478/535 # itn - 39/51
    files1 = os.listdir(pathA)
    files2 = os.listdir(pathB)
    docDistances = []

    weightsA = []
    weightsB = []

    sentenceDictA = getSentenceDict(inputpaths.enDataPath)
    sentenceDictB = getSentenceDict(inputpaths.siDataPath)

    for file1 in files1:
        weightsA.append(normalizeDocumentMass(getIDFWeightingsForFile(file1, inputpaths.enDataPath, sentenceDictA)))
    for file2 in files2:
        weightsB.append(normalizeDocumentMass(getIDFWeightingsForFile(file2, inputpaths.siDataPath, sentenceDictB)))

    tempDistances = []
    for i in range(len(files1)):
        # print(i)
        # if i == 500:
        #     print("breaking")
        #     break
        
        for j in range(len(files2)):
            weightA = weightsA[i].copy()
            weightB = weightsB[j].copy()
            tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB)})

    mergeSort(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    count = 0
    for matchedPair in matchedPairs:
        if matchedPair["a"] == matchedPair["b"]:
            count = count + 1
    print(matchedPairs)
    print("IDF count  : " + str(count))

def SLIDFAlignment(): # hiru -  328/500 after sentence split - 899/1216 # gossip - 296/300 # wsws - 300/300 # army - 521/535 # itn - 41/51
    files1 = os.listdir(pathA)
    files2 = os.listdir(pathB)
    docDistances = []

    weightsA = []
    weightsB = []

    sentenceDictA = getSentenceDict(inputpaths.enDataPath)
    sentenceDictB = getSentenceDict(inputpaths.siDataPath)

    tempweightA1 = []
    tempweightA2 = []
    tempweightB1 = []
    tempweightB2 = []

    for file1 in files1:
        tempweightA1.append(np.array(getSentenceLengthWeightings(file1, "en")))
        tempweightA2.append(np.array(getIDFWeightingsForFile(file1, inputpaths.enDataPath, sentenceDictA)))
    print("weights A")
    for file2 in files2:
        tempweightB2.append(np.array(getIDFWeightingsForFile(file2, inputpaths.siDataPath, sentenceDictB)))
        tempweightB1.append(np.array(getSentenceLengthWeightings(file2, "si")))
    print("weigths B")

    for i in range(len(tempweightA1)):
        weightsA.append(normalizeDocumentMass(tempweightA1[i] * tempweightA2[i]))
    for i in range(len(tempweightB1)):
        weightsB.append(normalizeDocumentMass(tempweightB1[i] * tempweightB2[i]))

    print("temp weights done")

    tempDistances = []
    for i in range(len(files1)):
        print("i",i)
        # if i == 300:
        #     print("breaking")
        #     break
        
        for j in range(len(files2)):
            # if j == 300:
            #     break
            weightA = weightsA[i].copy()
            weightB = weightsB[j].copy()
            tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB)})
    mergeSort(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    count = 0
    for matchedPair in matchedPairs:
        if matchedPair["a"] == matchedPair["b"]:
            count = count + 1
    print(matchedPairs)
    print("SLIDF count  : " + str(count))


def normalizeDocumentMass(fileWeights):
    total = sum(fileWeights)
    for i in range(len(fileWeights)):
        fileWeights[i] = fileWeights[i] / total
    return fileWeights


if __name__ == "__main__":
    main()
