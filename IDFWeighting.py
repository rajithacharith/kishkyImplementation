import os
import numpy as np
import inputpaths

def getSentenceDict(datapath):
    idfWeights = []
    sentenceDic = {}
    files = os.listdir(datapath)
    x=0
    for tempfile in files:
        # x=x+1
        # print(x)
        tempfile = open(datapath + tempfile)
        sentences = tempfile.readlines()
        for sentence in sentences:
            if sentence in sentenceDic:
                sentenceDic[sentence] = sentenceDic[sentence] + 1
            else:
                sentenceDic[sentence] = 1
        tempfile.close()
    idfDictionary = {}
    for tempfile in files:
        txtfile = open(datapath + tempfile)
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
    for count in idfDictionary[filename.replace("raw", "txt")]:
        weightings.append(1 + np.log((totalDocs + 1)/(1 + count)))
    return weightings

# crosslingual word 
# multilingual
# bilingual
# github repo eka cite krla tyeda balanna - lakmaligen ahanna