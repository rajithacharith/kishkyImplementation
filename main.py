import os
from GreedyMoversDistance import greedyMoversDistance
from SentenceLengthWeighting import getSentenceLengthWeightings
from MergeSort import mergeSort
from CompetitiveMatching import competitiveMatching
from IDFWeighting import getIDFWeightingsForFile, getSentenceDict
from DatewiseEvaluater import evaluateDatewise
import numpy as np
import inputpaths

embeddingPathA = inputpaths.enEmbeddingPath
embeddingPathB = inputpaths.siEmbeddingPath
datPathA = inputpaths.enDataPath
datPathB = inputpaths.siDataPath
paralleltxt = inputpaths.paralleltxt

def main():
    # sentenceLengthAlignment()
    # IDFAlignment()
    # SLIDFAlignment()
    runDatewise()

def runDatewise():
    alignedcounts = []
    totcounts = []
    enYears = os.listdir(embeddingPathA)
    for enYear in enYears:
        enMonths = os.listdir(embeddingPathA + enYear + "/")
        for enMonth in enMonths:
            enDays = os.listdir(embeddingPathA + enYear + "/" + enMonth + "/")
            for enDay in enDays:
                # sentence length
                matchedpairs = SentenceLengthAlignment(
                    embeddingPathA + enYear + "/" + enMonth + "/" + enDay + "/",
                    embeddingPathB + enYear + "/" + enMonth + "/" + enDay + "/",
                    datPathA + enYear + "/" + enMonth + "/" + enDay + "/",
                    datPathB + enYear + "/" + enMonth + "/" + enDay + "/"
                    )
                # idf
                # matchedpairs = IDFAlignment(
                #     embeddingPathA + enYear + "/" + enMonth + "/" + enDay + "/",
                #     embeddingPathB + enYear + "/" + enMonth + "/" + enDay + "/",
                #     datPathA + enYear + "/" + enMonth + "/" + enDay + "/",
                #     datPathB + enYear + "/" + enMonth + "/" + enDay + "/"
                #     )
                # slidf
                # matchedpairs = SLIDFAlignment(
                #     embeddingPathA + enYear + "/" + enMonth + "/" + enDay + "/",
                #     embeddingPathB + enYear + "/" + enMonth + "/" + enDay + "/",
                #     datPathA + enYear + "/" + enMonth + "/" + enDay + "/",
                #     datPathB + enYear + "/" + enMonth + "/" + enDay + "/"
                #     )
                print(enYear, enMonth, enDay)
                print(len(matchedpairs))
                result = evaluateDatewise(
                                paralleltxt,
                                matchedpairs
                                )
                alignedcounts.append(result[0])
                totcounts.append(result[1])
    # print(alignedcounts)
    # print(totcounts)
    print("Aligned count - " + str(sum(alignedcounts)))
    print("Total count - " + str(sum(totcounts)))

def SentenceLengthAlignment(embedPathA, embedPathB, dataPathA, dataPathB): # hiru -  325/500 # gosssip - 296/300 # wsws - 497/500 # army - 523/535 # itn - 41/51
    files1 = os.listdir(embedPathA)
    files2 = os.listdir(embedPathB)
    docDistances = []

    weightsA = []
    weightsB = []
    for file1 in files1:
        weightsA.append(normalizeDocumentMass(getSentenceLengthWeightings(dataPathA, file1)))
    for file2 in files2:
        weightsB.append(normalizeDocumentMass(getSentenceLengthWeightings(dataPathB, file2)))
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
            tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB, embedPathA, embedPathB)})

    mergeSort(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    count = 0
    for matchedPair in matchedPairs:
        if matchedPair["a"] == matchedPair["b"]:
            count = count + 1
    return matchedPairs

def IDFAlignment(embedPathA, embedPathB, dataPathA, dataPathB): # hiru - 281/500 # gosssip - 287/300 # army - 478/535 # itn - 39/51
    files1 = os.listdir(embedPathA)
    files2 = os.listdir(embedPathB)
    docDistances = []

    weightsA = []
    weightsB = []

    sentenceDictA = getSentenceDict(dataPathA)
    sentenceDictB = getSentenceDict(dataPathB)

    for file1 in files1:
        weightsA.append(normalizeDocumentMass(getIDFWeightingsForFile(file1, dataPathA, sentenceDictA)))
    for file2 in files2:
        weightsB.append(normalizeDocumentMass(getIDFWeightingsForFile(file2, dataPathB, sentenceDictB)))

    tempDistances = []
    for i in range(len(files1)):
        # print(i)
        # if i == 500:
        #     print("breaking")
        #     break
        
        for j in range(len(files2)):
            weightA = weightsA[i].copy()
            weightB = weightsB[j].copy()
            tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB, embedPathA, embedPathB)})

    mergeSort(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    count = 0
    for matchedPair in matchedPairs:
        if matchedPair["a"] == matchedPair["b"]:
            count = count + 1
    return matchedPairs

def SLIDFAlignment(embedPathA, embedPathB, dataPathA, dataPathB): # hiru -  328/500 after sentence split - 899/1216 # gossip - 296/300 # wsws - 300/300 # army - 521/535 # itn - 41/51
    files1 = os.listdir(embedPathA)
    files2 = os.listdir(embedPathB)
    docDistances = []

    weightsA = []
    weightsB = []

    sentenceDictA = getSentenceDict(dataPathA)
    sentenceDictB = getSentenceDict(dataPathB)

    tempweightA1 = []
    tempweightA2 = []
    tempweightB1 = []
    tempweightB2 = []

    for file1 in files1:
        tempweightA1.append(np.array(getSentenceLengthWeightings(dataPathA, file1)))
        tempweightA2.append(np.array(getIDFWeightingsForFile(file1, dataPathA, sentenceDictA)))
    # print("weights A")
    for file2 in files2:
        tempweightB2.append(np.array(getIDFWeightingsForFile(file2, dataPathB, sentenceDictB)))
        tempweightB1.append(np.array(getSentenceLengthWeightings(dataPathB, file2)))
    # print("weigths B")

    for i in range(len(tempweightA1)):
        weightsA.append(normalizeDocumentMass(tempweightA1[i] * tempweightA2[i]))
    for i in range(len(tempweightB1)):
        weightsB.append(normalizeDocumentMass(tempweightB1[i] * tempweightB2[i]))

    # print("temp weights done")

    tempDistances = []
    for i in range(len(files1)):
        # print("i",i)
        # if i == 300:
        #     print("breaking")
        #     break
        
        for j in range(len(files2)):
            # if j == 300:
            #     break
            weightA = weightsA[i].copy()
            weightB = weightsB[j].copy()
            tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB, embedPathA, embedPathB)})
    mergeSort(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    count = 0
    for matchedPair in matchedPairs:
        if matchedPair["a"] == matchedPair["b"]:
            count = count + 1
    # print(matchedPairs)
    # print("SLIDF count for " + dataPathA.split("/")[10] + " - " + dataPathA.split("/")[11] + " : " + str(count))
    return matchedPairs

def normalizeDocumentMass(fileWeights):
    total = sum(fileWeights)
    for i in range(len(fileWeights)):
        fileWeights[i] = fileWeights[i] / total
    return fileWeights


if __name__ == "__main__":
    main()
