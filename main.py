import os
from GreedyMoversDistance import greedyMoversDistance
from SentenceLengthWeighting import getSentenceLengthWeightings
from MergeSort import mergeSort
from CompetitiveMatching import competitiveMatching
from IDFWeighting import getIDFWeightingsForFile, getSentenceDict, getIDFWeightingForEquationEight, getIDFDictionaryWithNgrams, getTFDictionaryWithNgrams, getTFWeightsForFile
from DatewiseEvaluater import evaluateDatewise
import numpy as np
import inputpaths
import sys
import pickle

# embeddingPathA = inputpaths.embeddingPathA
# embeddingPathB = inputpaths.embeddingPathB
# datPathA = inputpaths.dataPathA
# datPathB = inputpaths.dataPathB
# paralleltxt = inputpaths.paralleltxt

embeddingPathA = ""
embeddingPathB = ""
datPathA = ""
datPathB = ""
paralleltxt = ""
option = ""
personNamesPathA = ""
personNamesPathB = ""
designationsPathA = ""
designationsPathB = ""
dictionaryPathA = ""
dictionaryPathB = ""
combined = 0

dim = 1024
# filename = '/home/dilan/Private/Projects/FYP/kishkyImplementation/model2_itm2.sav'
loaded_model = ""

dictDesigDictionary = {}
wordDictionary = {}

def main():
    global embeddingPathA
    global embeddingPathB
    global datPathA
    global datPathB
    global paralleltxt

    global loaded_model
    global option
    global dim

    global personNamesPathA
    global personNamesPathB
    global designationsPathA
    global designationsPathB
    global dictionaryPathA
    global dictionaryPathB
    global combined

    embeddingPathA = sys.argv[1]
    embeddingPathB = sys.argv[2]
    datPathA = sys.argv[3]
    datPathB = sys.argv[4]
    paralleltxt = sys.argv[5]
    mlModelPath = sys.argv[6]
    option = sys.argv[7]
    dim = int(sys.argv[8])
    personNamesPathA = sys.argv[9]
    personNamesPathB = sys.argv[10]
    designationsPathA = sys.argv[11]
    designationsPathB = sys.argv[12]
    dictionaryPathA = sys.argv[13]
    dictionaryPathB = sys.argv[14]
    combined = int(sys.argv[15])

    loaded_model = pickle.load(open(mlModelPath, 'rb'))

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
                # print(len(matchedpairs))
                # print(matchedpairs)
                result = evaluateDatewise(
                                paralleltxt,
                                matchedpairs
                                )
                alignedcounts.append(result[0])
                totcounts.append(result[1])
    # print(alignedcounts)
    # print(totcounts)
    print("Aligned count -", sum(alignedcounts))
    print("Total count -", sum(totcounts))

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
        for j in range(len(files2)):
            weightA = weightsA[i].copy()
            weightB = weightsB[j].copy()
            tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB, embedPathA, embedPathB, 
                wordDictionary, loaded_model, dataPathA, dataPathB, option, dim, dictDesigDictionary, combined)})

    mergeSort(tempDistances)
    print(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    # count = 0
    # for matchedPair in matchedPairs:
    #     if matchedPair["a"] == matchedPair["b"]:
    #         count = count + 1
    return matchedPairs

def IDFAlignment(embedPathA, embedPathB, dataPathA, dataPathB):
    try:
        files1 = os.listdir(embedPathA)
        files2 = os.listdir(embedPathB)
    except:
        return []
    docDistances = []

    weightsA = []
    weightsB = []

    # idfDictA = getIDFDictionaryWithNgrams(dataPathA, 6)
    # idfDictB = getIDFDictionaryWithNgrams(dataPathB, 6)

    # tfDictA = getTFDictionaryWithNgrams(dataPathA, 1)
    # tfDictB = getTFDictionaryWithNgrams(dataPathB, 1)

    # for file1 in files1:
    #     weightsA.append(normalizeDocumentMass(
    #         getTFWeightsForFile(
    #             file1,
    #             dataPathA,
    #             tfDictA,
    #             getIDFWeightingsForFile(file1, dataPathA, idfDictA)
    #         )
    #     ))
    # for file2 in files2:
    #     weightsB.append(normalizeDocumentMass(
    #         getTFWeightsForFile(
    #             file2,
    #             dataPathB,
    #             tfDictB,
    #             getIDFWeightingsForFile(file2, dataPathB, idfDictB)
    #         )
    #     ))

    sentenceDictA = getSentenceDict(dataPathA)
    sentenceDictB = getSentenceDict(dataPathB)

    for file1 in files1:
        weightsA.append(normalizeDocumentMass(
            getIDFWeightingsForFile(file1, dataPathA, sentenceDictA)
        ))
    for file2 in files2:
        weightsB.append(normalizeDocumentMass(
            getIDFWeightingsForFile(file2, dataPathB, sentenceDictB)
        ))

    tempDistances = []
    for i in range(len(files1)):
        for j in range(len(files2)):
            weightA = weightsA[i].copy()
            weightB = weightsB[j].copy()
            tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB, embedPathA, embedPathB, wordDictionary)})

    mergeSort(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    # count = 0
    # for matchedPair in matchedPairs:
    #     if matchedPair["a"] == matchedPair["b"]:
    #         count = count + 1
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

    sentenceDictA = getSentenceDict(dataPathA)
    sentenceDictB = getSentenceDict(dataPathB)

    # idfDictA = getIDFDictionaryWithNgrams(dataPathA, 6)
    # idfDictB = getIDFDictionaryWithNgrams(dataPathB, 6)

    # tfDictA = getTFDictionaryWithNgrams(dataPathA, 1)
    # tfDictB = getTFDictionaryWithNgrams(dataPathB, 1)

    tempweightA1 = []
    tempweightA2 = []
    tempweightB1 = []
    tempweightB2 = []

    for file1 in files1:
        tempweightA1.append(np.array(getSentenceLengthWeightings(dataPathA, file1, 'en')))
        # tempweightA2.append(normalizeDocumentMass(
        #     getTFWeightsForFile(
        #         file1,
        #         dataPathA,
        #         tfDictA,
        #         getIDFWeightingsForFile(file1, dataPathA, idfDictA)
        #     )
        # ))
        tempweightA2.append(
            getIDFWeightingsForFile(file1, dataPathA, sentenceDictA)
        )
        # tempweightA2.append(np.array(getIDFWeightingForEquationEight(file1, dataPathA, sentenceDictA)))
    # print("weights A")
    for file2 in files2:
        tempweightB1.append(np.array(getSentenceLengthWeightings(dataPathB, file2, 'ta')))
        # tempweightB2.append(normalizeDocumentMass(
        #     getTFWeightsForFile(
        #         file2,
        #         dataPathB,
        #         tfDictB,
        #         getIDFWeightingsForFile(file2, dataPathB, idfDictB)
        #     )
        # ))
        tempweightB2.append(
            getIDFWeightingsForFile(file2, dataPathB, sentenceDictB)
        )
        # tempweightB2.append(np.array(getIDFWeightingForEquationEight(file2, dataPathB, sentenceDictB)))
    # print("weigths B")

    for i in range(len(tempweightA1)):
        weightsA.append(normalizeDocumentMass(tempweightA1[i] * tempweightA2[i]))
    for i in range(len(tempweightB1)):
        weightsB.append(normalizeDocumentMass(tempweightB1[i] * tempweightB2[i]))

    tempDistances = []
    for i in range(len(files1)):
        # print("i",i)
        for j in range(len(files2)):
            weightA = weightsA[i].copy()
            weightB = weightsB[j].copy()
            tempDistances.append({"a": files1[i], "b": files2[j], "distance": greedyMoversDistance(files1[i], files2[j], weightA, weightB, embedPathA, embedPathB, wordDictionary)})
    mergeSort(tempDistances)
    matchedPairs = competitiveMatching(tempDistances)

    # count = 0
    # for matchedPair in matchedPairs:
    #     if matchedPair["a"] == matchedPair["b"]:
    #         count = count + 1
    # print(matchedPairs)
    # print("SLIDF count for " + dataPathA.split("/")[10] + " - " + dataPathA.split("/")[11] + " : " + str(count))
    return matchedPairs

def normalizeDocumentMass(fileWeights):
    total = sum(fileWeights)
    for i in range(len(fileWeights)):
        fileWeights[i] = fileWeights[i] / total
    return fileWeights

def loadDictionaries():
    # sitasiNameSet = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-ta lists/uniq_names.tok.si-ta.si", "r")
    # sitataNameSet = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-ta lists/uniq_names.tok.si-ta.ta", "r")

    # wordsA = open(inputpaths.existingDictionaryA).readlines()
    # wordsB = open(inputpaths.existingDictionaryB).readlines()
    
    namesA = open(personNamesPathA).readlines()
    namesB = open(personNamesPathB).readlines()

    # for i in range(len(wordsA)):
    #     wordA = wordsA[i].strip().replace("\n", "")
    #     if (wordDictionary.get(wordA, False)):
    #         wordDictionary[wordA].append(wordsB[i].strip().replace("\n", ""))
    #     else:
    #         wordDictionary[wordA]  = [wordsB[i].strip().replace("\n", "")]
    for  i in range(len(namesA)):
        nameA = namesA[i].strip().replace("\n", "")
        if (wordDictionary.get(nameA, False)):
            wordDictionary[nameA].append(namesB[i].strip().replace("\n", ""))
        else:
            wordDictionary[nameA] = [namesB[i].strip().replace("\n", "")]

    
    with open(designationsPathA) as designationsFileA:
        with open(designationsPathB) as designationsFileB:
            linesA = designationsFileA.readlines()
            linesB = designationsFileB.readlines()
            for i in range(len(linesA)):
                word = linesA[i].strip().replace("\n", "").lower()
                if (dictDesigDictionary.get(word, False)):
                    dictDesigDictionary[word].append(linesB[i].strip().replace("\n", ""))
                else:
                    dictDesigDictionary[word]  = [linesB[i].strip().replace("\n", "")]

    with open(dictionaryPathA) as dictionaryFileA:
        with open(dictionaryPathB) as dictionaryFileB:
            linesA = dictionaryFileA.readlines()
            linesB = dictionaryFileB.readlines()
            for i in range(len(linesA)):
                word = linesA[i].strip().replace("\n", "").lower()
                if (dictDesigDictionary.get(word, False)):
                    if (linesB[i].strip().replace("\n", "") not in dictDesigDictionary.get(word)):
                        dictDesigDictionary[word].append(linesB[i].strip().replace("\n", ""))
                else:
                    dictDesigDictionary[word]  = [linesB[i].strip().replace("\n", "")]

if __name__ == "__main__":
    main()