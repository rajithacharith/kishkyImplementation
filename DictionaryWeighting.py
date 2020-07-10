# wordDictionary = {}

# def loadDictionaries():
#     enDictionary = open("./en-si-dictionary/dic-unique-terms-30.12.2019.en", "r")
#     siDictionary = open("./en-si-dictionary/dic-unique-terms-30.12.2019.si", "r")
#     enWords = enDictionary.readlines()
#     siWords = siDictionary.readlines()
#     for i in range(len(enWords)):
#         wordDictionary[enWords[i].strip().replace("\n", "")] = siWords[i].strip().replace("\n", "")


enDesigList = []
siDesigList = []
enDesigDic = {}

print("creating desig list")
# with open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-en lists/designation.en", "r") as tempfile1:
with open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/ta-en lists/designation.en", "r") as tempfile1:
    # with open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/si-en lists/designation.si", "r") as tempfile2:
    with open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/ta-en lists/designation.ta", "r") as tempfile2:
        enlines = tempfile1.readlines()
        silines = tempfile2.readlines()
        # for line in enlines:
        #     enDesigList.append(line.strip().replace("\n", "").lower())
        # for line in silines:
        #     siDesigList.append(line.strip().replace("\n", "").lower())
        for i in range(len(enlines)):
            enDesigDic[enlines[i].strip().replace("\n", "").lower()] = silines[i].strip().replace("\n", "")
# print(enDesigDic)

def calcDictionaryWeight(fileA, fileB, pathA, pathB, wordDictionary):
    docA = open(pathA.replace("Embeddings", "Data-Formatted") + fileA.replace("raw", "txt"), "r")
    docB = open(pathB.replace("Embeddings", "Data-Formatted") + fileB.replace("raw", "txt"), "r")
    enLines = docA.readlines()
    siLines = docB.readlines()
    enWords = []
    siWords = []
    for enLine in enLines:
        enWords = enWords + enLine.split()
    for siLine in siLines:
        siWords = siWords + siLine.split()
    for i in range(len(enWords)):
        enWords[i] = enWords[i].strip().replace(".", "").replace(",", "").lower()
    for i in range(len(siWords)):
        siWords[i] = siWords[i].strip().replace(".", "").replace(",", "")
    count = 1
    for enWord in enWords:
        value = wordDictionary.get(enWord, False)
        if (value != False):
            if (value in siWords):
                count = count + 1
                siWords.remove(value)
                # print("en word: ", enWord, "si word: ", value)
    # return ((len(siWords) + len(enWords)) / (count * 2))
    # return ((count * 2) / (len(siWords) + len(enWords)))
    if (count > 10):
        # print(count)
        # print(enWords)
        # print(siWords)
        # print()
        return 0.2
    elif (count > 8):
        return 0.4
    elif (count > 6):
        return 0.6
    elif (count > 4):
        return 0.8
    else:
        return 1
    # return 1/count

# def checkDesignations(enLine, siLine):
#     count = 1
#     for i in range(len(enDesigList)):
#         if (enDesigList[i] in enLine):
#             if (siDesigList[i] in siLine):
#                 count = count + len(enDesigList[i])
#                 print(count)
#                 print(enDesigList[i], siDesigList[i])
#     return count

def checkDesignations(enLine, siLine):
    count = 1
    enWords = enLine.strip().replace("\n", "").replace(".", "").lower().split()
    siLine = siLine.strip().replace("\n", "")

    if (len(enWords) > 3):
        for i in range(1, 5):
            for j in range(0, len(enWords) - (i - 1)):
                x = " ".join(enWords[j: j + i])
                y = enDesigDic.get(x, False)
                if (y):
                    if (y in siLine):
                        count = count + len(x.split())
    else:
        for i in range(1, len(enWords) + 1):
            for j in range(0, len(enWords) - (i - 1)):
                x = " ".join(enWords[j: j + i])
                y = enDesigDic.get(x, False)
                if (y):
                    if (y in siLine):
                        count = count + len(x.split())
    return count

def calcDicWeightForLine(enLine, siLine, wordDictionary):
    count = checkDesignations(enLine, siLine)
    enWords = enLine.split()
    siWords = siLine.split()
    for i in range(len(enWords)):
        enWords[i] = enWords[i].strip().replace(".", "").replace(",", "").lower()
    for i in range(len(siWords)):
        siWords[i] = siWords[i].strip().replace(".", "").replace(",", "")
    for enWord in enWords:
        value = wordDictionary.get(enWord, False)
        if (value != False):
            if (value in siWords):
                count = count + 1
                siWords.remove(value)
    return (len(enWords) - count)/len(enWords)
