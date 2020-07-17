wordDictionary = {}

# def createDictionaryFromSiTa():
#     loadDictionaries()
#     sitasidic = open("./DMS/smt_nmt_datasets/si-ta lists/dic.tok-cl3.19-02-2020.si-ta.si", "r")
#     sitatadic = open("./DMS/smt_nmt_datasets/si-ta lists/dic.tok-cl3.19-02-2020.si-ta.ta", "r")

#     sitasiwords = sitasidic.readlines()
#     sitatawords = sitatadic.readlines()
#     for i in range(len(sitasiwords)):
#         word = sienwordDictionary.get(sitasiwords[i].strip().replace("\n", ""), False)
#         if (word):
#             entawordDictionary[word.strip().replace("\n", "")] = sitatawords[i].strip().replace("\n", "")
#     print(entawordDictionary)
#     print(len(entawordDictionary))


def loadDictionaries():
    enDictionary = open("/home/dilan/Private/Projects/tamil_dictionary/ta-en-dic.en", "r")
    taDictionary = open("/home/dilan/Private/Projects/tamil_dictionary/ta-en-dic.ta", "r")
    enWords = enDictionary.readlines()
    taWords = taDictionary.readlines()
    for i in range(len(enWords)):
        wordDictionary[taWords[i].strip().replace("\n", "")] = enWords[i].strip().replace("\n", "")


def mapWords(enWords, taLine):
    enLine = " ".join(enWords)
    for i in range(0, len(enWords)):
        taword = wordDictionary.get(enWords[i], False)
        if (taword):
            if (taword in taLine):
                print(taword)
                print(enWords[i])
                print()
                taLine = taLine.replace(taword, "")
                enLine = enLine.replace(enWords[i], "")
    taLine = " ".join(taLine.strip().split())
    enLine = " ".join(enLine.strip().split())
    # print(siLine)
    # print(enLine)
    # print()
    wordDictionary[enLine] = taLine

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

with open("./glossary/en-ta/combinedGlossary.en", "w") as enwritefile:
    with open("./glossary/en-ta/combinedGlossary.ta", "w") as tawritefile:
        for key, value in wordDictionary.items():
            enwritefile.write(key + "\n")
            tawritefile.write(value + "\n")