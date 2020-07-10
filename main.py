import os
from GreedyMoversDistance import greedyMoversDistance
from SentenceLengthWeighting import getSentenceLengthWeightings
from MergeSort import mergeSort
from CompetitiveMatching import competitiveMatching
from IDFWeighting import getIDFWeightingsForFile, getSentenceDict, getIDFWeightingForEquationEight, getIDFDictionaryWithNgrams, getTFDictionaryWithNgrams, getTFWeightsForFile
from DatewiseEvaluater import evaluateDatewise
import numpy as np
import inputpaths

embeddingPathA = inputpaths.enEmbeddingPath
# embeddingPathB = inputpaths.siEmbeddingPath
embeddingPathB = inputpaths.taEmbeddingPath
datPathA = inputpaths.enDataPath
# datPathB = inputpaths.siDataPath
datPathB = inputpaths.taDataPath
# paralleltxt = inputpaths.ensiparalleltxt
paralleltxt = inputpaths.entaparalleltxt

wordDictionary = {}

def main():
    loadDictionaries()
    runDatewise()
    # runcombined()

def runcombined():
    # matchedpairs = SLIDFAlignment(embeddingPathA, embeddingPathB, datPathA, datPathB)
    matchedpairs = SentenceLengthAlignment(embeddingPathA, embeddingPathB, datPathA, datPathB)
    print(matchedpairs)
    results = evaluateDatewise(paralleltxt, matchedpairs)
    print("Aligned count - " + str(results[0]))
    print("Total count - " + str(results[1]))

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
                # print(matchedpairs)
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
    try:
        files1 = os.listdir(embedPathA)
        files2 = os.listdir(embedPathB)
    except:
        return []
    docDistances = []

    weightsA = []
    weightsB = []
    for file1 in files1:
        weightsA.append(normalizeDocumentMass(getSentenceLengthWeightings(dataPathA, file1, 'en')))
    for file2 in files2:
        weightsB.append(normalizeDocumentMass(getSentenceLengthWeightings(dataPathB, file2, 'ta')))
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
            tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB, embedPathA, embedPathB, wordDictionary)})

    mergeSort(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    count = 0
    for matchedPair in matchedPairs:
        if matchedPair["a"] == matchedPair["b"]:
            count = count + 1
    return matchedPairs

def IDFAlignment(embedPathA, embedPathB, dataPathA, dataPathB): # hiru - 281/500 # gosssip - 287/300 # army - 478/535 # itn - 39/51
    try:
        files1 = os.listdir(embedPathA)
        files2 = os.listdir(embedPathB)
    except:
        return []
    docDistances = []

    weightsA = []
    weightsB = []

    # sentenceDictA = getSentenceDict(dataPathA)
    # sentenceDictB = getSentenceDict(dataPathB)

    idfDictA = getIDFDictionaryWithNgrams(dataPathA, 6)
    idfDictB = getIDFDictionaryWithNgrams(dataPathB, 6)

    tfDictA = getTFDictionaryWithNgrams(dataPathA, 1)
    tfDictB = getTFDictionaryWithNgrams(dataPathB, 1)

    for file1 in files1:
        weightsA.append(normalizeDocumentMass(
            getTFWeightsForFile(
                file1,
                dataPathA,
                tfDictA,
                getIDFWeightingsForFile(file1, dataPathA, idfDictA)
            )
        ))
    for file2 in files2:
        weightsB.append(normalizeDocumentMass(
            getTFWeightsForFile(
                file2,
                dataPathB,
                tfDictB,
                getIDFWeightingsForFile(file2, dataPathB, idfDictB)
            )
        ))

    tempDistances = []
    for i in range(len(files1)):
        # print(i)
        # if i == 500:
        #     print("breaking")
        #     break
        
        for j in range(len(files2)):
            weightA = weightsA[i].copy()
            weightB = weightsB[j].copy()
            tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB, embedPathA, embedPathB, wordDictionary)})

    mergeSort(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    count = 0
    for matchedPair in matchedPairs:
        if matchedPair["a"] == matchedPair["b"]:
            count = count + 1
    return matchedPairs

def SLIDFAlignment(embedPathA, embedPathB, dataPathA, dataPathB):
    try:
        files1 = os.listdir(embedPathA)
        files2 = os.listdir(embedPathB)
    except:
        return []
    docDistances = []

    weightsA = []
    weightsB = []

    # sentenceDictA = getSentenceDict(dataPathA)
    # sentenceDictB = getSentenceDict(dataPathB)

    idfDictA = getIDFDictionaryWithNgrams(dataPathA, 6)
    idfDictB = getIDFDictionaryWithNgrams(dataPathB, 6)

    tfDictA = getTFDictionaryWithNgrams(dataPathA, 1)
    tfDictB = getTFDictionaryWithNgrams(dataPathB, 1)

    tempweightA1 = []
    tempweightA2 = []
    tempweightB1 = []
    tempweightB2 = []

    for file1 in files1:
        tempweightA1.append(np.array(getSentenceLengthWeightings(dataPathA, file1, 'en')))
        tempweightA2.append(normalizeDocumentMass(
            getTFWeightsForFile(
                file1,
                dataPathA,
                tfDictA,
                getIDFWeightingsForFile(file1, dataPathA, idfDictA)
            )
        ))
        # tempweightA2.append(np.array(getIDFWeightingForEquationEight(file1, dataPathA, sentenceDictA)))
    # print("weights A")
    for file2 in files2:
        tempweightB1.append(np.array(getSentenceLengthWeightings(dataPathB, file2, 'ta')))
        tempweightB2.append(normalizeDocumentMass(
            getTFWeightsForFile(
                file2,
                dataPathB,
                tfDictB,
                getIDFWeightingsForFile(file2, dataPathB, idfDictB)
            )
        ))
        # tempweightB2.append(np.array(getIDFWeightingForEquationEight(file2, dataPathB, sentenceDictB)))
    # print("weigths B")

    for i in range(len(tempweightA1)):
        weightsA.append(normalizeDocumentMass(tempweightA1[i] * tempweightA2[i]))
    for i in range(len(tempweightB1)):
        weightsB.append(normalizeDocumentMass(tempweightB1[i] * tempweightB2[i]))

    tempDistances = []
    for i in range(len(files1)):
        print("i",i)
        for j in range(len(files2)):
            weightA = weightsA[i].copy()
            weightB = weightsB[j].copy()
            tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB, embedPathA, embedPathB, wordDictionary)})
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

def loadDictionaries():
    # enDictionary = open("./glossary/combinedGlossary.en", "r")
    # siDictionary = open("./glossary/combinedGlossary.si", "r")
    # taDictionary = open("./glossary/combinedGlossary.ta", "r")
    # enDictionary = open("./aug-en-si-dictionary/augDic-nonNoun-terms.en", "r")
    # siDictionary = open("./aug-en-si-dictionary/augDic-nonNoun-terms.si", "r")
    enDictionary = open("./DMS/smt_nmt_datasets/parallel-corpus/glossary_unique-19.02.2020.en", "r")
    taDictionary = open("./DMS/smt_nmt_datasets/parallel-corpus/glossary_unique-19.02.2020.ta", "r")
    # ensienNameSet = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-en lists/person-names.en", "r")
    # ensisiNameSet = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-en lists/person-names.si", "r")
    entaenNameSet = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/ta-en lists/person-names.en", "r")
    entataNameSet = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/ta-en lists/person-names.ta", "r")

    enWords = enDictionary.readlines()
    siWords = taDictionary.readlines()
    
    enNames = entaenNameSet.readlines()
    siNames = entataNameSet.readlines()

    for i in range(len(enWords)):
        wordDictionary[enWords[i].strip().replace("\n", "")] = siWords[i].strip().replace("\n", "")
    for  i in range(len(enNames)):
        wordDictionary[enNames[i].strip().replace("\n", "")] = siNames[i].strip().replace("\n", "")
    # print(wordDictionary)

if __name__ == "__main__":
    main()
# mine - 1173, aloka - 1167, aloka with desing - 1181, mine with desig - 1185
# metric learning + new glossary + designation - 1215