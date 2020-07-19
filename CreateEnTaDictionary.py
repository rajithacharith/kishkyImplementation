wordDictionary = {}

def loadDictionaries():
    enDictionary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/Dictionaries/EN-TA/existingdictionary.en", "r")
    taDictionary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/Dictionaries/EN-TA/existingdictionary.ta", "r")
    enWords = enDictionary.readlines()
    taWords = taDictionary.readlines()
    for i in range(len(enWords)):
        enword = enWords[i].strip().replace("\n", "")
        if (wordDictionary.get(enword, False)):
            wordDictionary[enword].append(taWords[i].strip().replace("\n", ""))
        else:
            wordDictionary[enword]  = [taWords[i].strip().replace("\n", "")]


def mapWords(enWords, taLine):
    enLine = " ".join(enWords)
    for i in range(0, len(enWords)):
        tawords = wordDictionary.get(enWords[i], False)
        if (tawords):
            for taword in tawords:
                if (taword in taLine):
                    taLine = taLine.replace(taword, "")
                    enLine = enLine.replace(enWords[i], "")
    taLine = " ".join(taLine.strip().split())
    enLine = " ".join(enLine.strip().split())
    wordDictionary[enLine] = [taLine]

################################
# execution
################################

loadDictionaries()

enGlossary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/parallel-corpus/glossary_unique-19.02.2020.en", "r")
taGlossary = open("/home/dilan/Private/Projects/FYP/kishkyImplementation/DMS/smt_nmt_datasets/parallel-corpus/glossary_unique-19.02.2020.ta", "r")

enGlossWords = enGlossary.readlines()
taGlossWords = taGlossary.readlines()

for i in range(len(enGlossWords)):
    words = enGlossWords[i].strip().replace("\n", "").lower().split()
    mapWords(words, taGlossWords[i].strip().replace("\n", ""))

with open("./Dictionaries/EN-TA/combinedGlossary.en", "w") as enwritefile:
    with open("./Dictionaries/EN-TA/combinedGlossary.ta", "w") as tawritefile:
        for key, values in wordDictionary.items():
            for value in values:
                enwritefile.write(key + "\n")
                tawritefile.write(value + "\n")
            print(key, values)