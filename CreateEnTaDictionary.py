
sienwordDictionary = {}
entawordDictionary = {}

def createDictionaryFromSiTa():
    loadDictionaries()
    sitasidic = open("./DMS/smt_nmt_datasets/si-ta lists/dic.tok-cl3.19-02-2020.si-ta.si", "r")
    sitatadic = open("./DMS/smt_nmt_datasets/si-ta lists/dic.tok-cl3.19-02-2020.si-ta.ta", "r")

    sitasiwords = sitasidic.readlines()
    sitatawords = sitatadic.readlines()
    for i in range(len(sitasiwords)):
        word = sienwordDictionary.get(sitasiwords[i].strip().replace("\n", ""), False)
        if (word):
            entawordDictionary[word.strip().replace("\n", "")] = sitatawords[i].strip().replace("\n", "")
    print(entawordDictionary)
    print(len(entawordDictionary))


def loadDictionaries():
    enDictionary = open("./en-si-dictionary/dic-unique-terms-30.12.2019.en", "r")
    siDictionary = open("./en-si-dictionary/dic-unique-terms-30.12.2019.si", "r")
    # enDictionary = open("./aug-en-si-dictionary/augDic-nonNoun-terms.en", "r")
    # siDictionary = open("./aug-en-si-dictionary/augDic-nonNoun-terms.si", "r")
    enWords = enDictionary.readlines()
    siWords = siDictionary.readlines()
    for i in range(len(enWords)):
        sienwordDictionary[siWords[i].strip().replace("\n", "")] = enWords[i].strip().replace("\n", "")


createDictionaryFromSiTa()

# def mapWords(enWords, siLine):
#     enLine = " ".join(enWords)
#     for i in range(0, len(enWords)):
#         siword = wordDictionary.get(enWords[i], False)
#         if (siword):
#             if (siword in siLine):
#                 print(siword)
#                 print(enWords[i])
#                 print()
#                 siLine = siLine.replace(siword, "")
#                 enLine = enLine.replace(enWords[i], "")
#     siLine = " ".join(siLine.strip().split())
#     enLine = " ".join(enLine.strip().split())
#     # print(siLine)
#     # print(enLine)
#     # print()
#     wordDictionary[enLine] = siLine

# ################################
# # execution
# ################################

# loadDictionaries()

# enGlossary = open("./glossary/glossary-06.11.2019.en", "r")
# siGlossary = open("./glossary/glossary-06.11.2019.si", "r")

# enGlossWords = enGlossary.readlines()
# siGlossWords = siGlossary.readlines()

# for i in range(len(enGlossWords)):
#     words = enGlossWords[i].strip().replace("\n", "").lower().split()
#     mapWords(words, siGlossWords[i].strip().replace("\n", ""))

# with open("./glossary/combinedGlossary.en", "w") as enwritefile:
#     with open("./glossary/combinedGlossary.si", "w") as siwritefile:
#         for key, value in wordDictionary.items():
#             enwritefile.write(key + "\n")
#             siwritefile.write(value + "\n")