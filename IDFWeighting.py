import os
import numpy as np
import inputpaths

temppathA = inputpaths.enEmbeddingPath
temppathB = inputpaths.siEmbeddingPath

def getSentenceDict(path):
    idfWeights = []
    sentenceDic = {}
    files = []
    if "/en/" in path:
        files = os.listdir(temppathA)
    if "/si/" in path:
        files = os.listdir(temppathB)
    x=0
    for tempfile in files:
        # x=x+1
        # print(x)
        tempfile = open(path + tempfile.replace("raw", "txt"))
        sentences = tempfile.readlines()
        for sentence in sentences:
            if sentence in sentenceDic:
                sentenceDic[sentence] = sentenceDic[sentence] + 1
            else:
                sentenceDic[sentence] = 1
        tempfile.close()
    idfDictionary = {}
    for tempfile in files:
        txtfile = open(path + tempfile.replace("raw", "txt"))
        idfDictionary[tempfile] = []
        sentences = txtfile.readlines()
        for sentence in sentences:
            idfDictionary[tempfile].append(sentenceDic[sentence])
        txtfile.close()
    return idfDictionary

def getIDFWeightingsForFile(filename, path, idfDictionary):
    weightings = []
    tempfile = open(path + filename.replace("raw", "txt"), "r")
    sentences = tempfile.readlines()
    # totalDocs = len(os.listdir(path))
    totalDocs = 3000
    # print(idfDictionary)
    for count in idfDictionary[filename]:
        weightings.append(1 + np.log((totalDocs + 1)/(1 + count)))
    return weightings

