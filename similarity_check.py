import os
import json
from random import randrange
import csv
from sentence_splitter import SentenceSplitter, split_text_into_sentences
import sys

sys.path.insert(0, "../../sinling/sinling/sinhala/")

from tokenizer import SinhalaTokenizer

sinhalasplitter = SinhalaTokenizer()
englishsplitter = SentenceSplitter(language='en')


# a = "`මධ්‍යම ආරක්‍ෂක සේනා මූලස්ථානය යටතේ සේවයෙන් නියුතු යුද්ධ හමුදා නිලධාරින් සඳහා ‘අන්තර් ජාතික මානූෂිය නීතිය’ පිළිබඳ වැඩමුළුවක් බදාදා (31) වන දින දියතලාව ස්වේච්ඡා බලසේනා පුහුණු පාසල (VFTS) හිදී පැවැත්වියූ. ඒ සඳහා 112 වන බලසේනාවේ බළසේනාධිපති බ්‍රිගේඩියර් එම්. ඩබ්. ඒ. ඒ. විජේසූරිය සහ 121 වන බලසේනාවේ බළසේනාධිපති බ්‍රිගේඩියර් එන්. සී. සෝමවීර ඇතුළු යුද්ධ හමුදා නිලධාරීන් 20 ක් මෙම වැඩමුළුව සඳහා සහභාගී වුහ. මෙම වැඩමුළුව රතු කුරුස සංවිධානයේ කලාපීය සහ ආරක්‍ෂක හමුදා නියෝජිතයා වන ජැක් ලෙමා මහතා (Mr Jacques Lemay) සහ රතු කුරුස සංවිධානයේ සන්නිවේදන නිලධාරි චන්න ජයවර්ධන යන මහත්වරුන් විසින් මෙහෙයවනු ලැබීය."
# print(sinhalasplitter.split_sentences(a))
# print(len(sinhalasplitter.split_sentences(a)))

def convertToEmbedding(readpath, writepath, lang):
    os.system("${LASER}/tasks/embed/embed.sh " + readpath + " " + lang + " " + writepath)

def formatFileForEmbedding(readpath, writepath, lang):
    try:
        content = ""
        with open(readpath) as document:
            doc = json.load(document)
            content = doc["Content"]
            if len(content) == 0:
                return
        sentences = []
        for line in content:
            if (lang == "en"):
                sentences = sentences + englishsplitter.split(text = line)
            elif (lang == "si"):
                sentences = sentences + sinhalasplitter.split_sentences(line)
        # sentences = sentences + content.split(".")
        # print(sentences)
        writefile = open(writepath, "w")
        for sentence in sentences:
            if sentence != "" and sentence != " " and sentence != "\n":
                writesent = sentence.strip().replace("\n", "")
                if writesent != "" and writesent != " ":
                    writefile.write(writesent)
                    writefile.write("\n")
        writefile.close()
    except Exception:
        print(readpath)

def formatArmyFileForEmbedding(readpath, writepath, lang):
    # try:
    content = ""
    with open(readpath) as document:
        doc = json.load(document)
        content = doc["Content"]
        if len(content) == 0:
            return
    sentences = []
    if (lang == "en"):
        sentences = sentences + englishsplitter.split(text = content)
    elif (lang == "si"):
        sentences = sentences + sinhalasplitter.split_sentences(content)
    # print(sentences)
    writefile = open(writepath, "w")
    for sentence in sentences:
        if sentence != "" and sentence != " " and sentence != "\n":
            writesent = sentence.strip().replace("\n", "")
            if writesent != "" and writesent != " ":
                writefile.write(writesent)
                writefile.write("\n")
    writefile.close()
    # except Exception:
    #     print(readpath)

def formatFiles(path, writepath):
    files = os.listdir(path)
    for file in files:
        formatFileForEmbedding((path + file), (writepath + str(randrange(100000000)) + ".txt"))

def createEmbeddings(path, writepath, lang):
    files = os.listdir(path)
    print(files)
    a = 0
    for file in files:
        convertToEmbedding((path + file), (writepath + file.replace("txt", "raw")), lang)
        # a = a + 1
        # if a == 300:
            # break

def getFromHiruFolder():
    sinhalafiles = os.listdir("/home/dilan/Private/Projects/FYP/Data-ToFormat/date_split/sinhala/January/01/")
    englishfiles = os.listdir("/home/dilan/Private/Projects/FYP/Data-ToFormat/date_split/english/January/01/")
    for sinhalafile in sinhalafiles:
        if sinhalafile in englishfiles:
            formatFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/date_split/sinhala/January/01/"+sinhalafile, "/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/hiru/si/" + sinhalafile.replace(".json", ".txt"), "si")
            formatFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/date_split/english/January/01/"+sinhalafile, "/home/dilan/Private/Projects/FYP/Data-Formatted/datewise/hiru/en/" + sinhalafile.replace(".json", ".txt"), "en")

def getFromWswsFolder():
    sinhalafiles = os.listdir("/home/dilan/Downloads/New/wswssinhalaparallel/sinhala_parallel/sinhala/")
    englishfiles = os.listdir("/home/dilan/Downloads/New/wswssinhalaparallel/sinhala_parallel/english/")
    for englishfile in englishfiles:
        formatFileForEmbedding("/home/dilan/Downloads/New/wswssinhalaparallel/sinhala_parallel/sinhala/" + englishfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/wsws/si/" + englishfile.replace("json", "txt"), "si")
        formatFileForEmbedding("/home/dilan/Downloads/New/wswssinhalaparallel/sinhala_parallel/english/" + englishfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/wsws/en/" + englishfile.replace("json", "txt"), "en")

def getFromWikipediaFolder():
    sinhalafiles = os.listdir("/home/dilan/Downloads/New/wikipediasinhala/sinhala/")
    englishfiles = os.listdir("/home/dilan/Downloads/New/wikipediaengilsh/english/")
    for englishfile in englishfiles:
        formatFileForEmbedding("/home/dilan/Downloads/New/wikipediasinhala/sinhala/" + englishfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/wikipedia/si/" + englishfile.replace("json", "txt"), "si")
        formatFileForEmbedding("/home/dilan/Downloads/New/wikipediaengilsh/english/" + englishfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/wikipedia/en/" + englishfile.replace("json", "txt"), "si")

def getFromArmyFolder():
    csvpath = "/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/"
    sinhalafiles = "/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/Sinhala/"
    englishfiles = "/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/English/"
    sifiles = os.listdir(sinhalafiles)
    enfiles = os.listdir(englishfiles)
    enfilenames = []
    sifilenames = []
    with open(csvpath + "golden_alignment.txt") as csvfile:
        csvReader = csv.reader(csvfile, delimiter = "|")
        for row in csvReader:
            sifilenames.append(row[0].strip())
            enfilenames.append(row[2].strip()) 
    for sinfile in sifiles:
        if sinfile in sifilenames:
            print("yes")
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/Sinhala/" + sinfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/army/si/" + str(sifilenames.index(sinfile)) + ".txt", "si")
        else:
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/Sinhala/" + sinfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/army/si/" + sinfile.replace(".json", ".txt"), "si")
    for enfile in enfiles:
        if enfile in enfilenames:
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/English/" + enfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/army/en/" + str(enfilenames.index(enfile)) + ".txt", "en")
        else:
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/army/Army_news/English/" + enfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/army/en/" + enfile.replace(".json", ".txt"), "en")


def getFromITNFolder():
    csvpath = "/home/dilan/Private/Projects/FYP/Data-ToFormat/itn/Testing/"
    sinhalafiles = "/home/dilan/Private/Projects/FYP/Data-ToFormat/itn/Testing/Sinhala/"
    englishfiles = "/home/dilan/Private/Projects/FYP/Data-ToFormat/itn/Testing/English/"
    sifiles = os.listdir("/home/dilan/Private/Projects/FYP/Data-ToFormat/itn/Testing/Sinhala/")
    enfiles = os.listdir("/home/dilan/Private/Projects/FYP/Data-ToFormat/itn/Testing/English/")
    enfilenames = []
    sifilenames = []
    with open(csvpath + "golden_alignment.txt") as csvfile:
        csvReader = csv.reader(csvfile, delimiter = "|")
        for row in csvReader:
            # if " "+row[0].strip() in files:
            #     print("present")
            #     print(row[0].strip())
            sifilenames.append(row[0].strip())
            enfilenames.append(row[2].strip())
    for sifile in sifiles:
        a = False
        for i in range(len(sifilenames)):
            if sifile.strip() == sifilenames[i]:
                formatArmyFileForEmbedding(sinhalafiles + sifile, "/home/dilan/Private/Projects/FYP/Data-Formatted/itn/si/" + str(i) + ".txt", "si")
                a = True
        if a == False:
            formatArmyFileForEmbedding(sinhalafiles +sifile, "/home/dilan/Private/Projects/FYP/Data-Formatted/itn/si/" + str(randrange(10000000)) + ".txt", "si")
    for enfile in enfiles:
        a = False
        for i in range(len(enfilenames)):
            if enfile.strip() == enfilenames[i]:
                formatArmyFileForEmbedding(englishfiles + enfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/itn/en/" + str(i) + ".txt", "en")
                a = True
        if a == False:
            formatArmyFileForEmbedding(englishfiles + enfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/itn/en/" + str(randrange(10000000)) + ".txt", "en")

def readCsvGossipLanka():
    csvpath = "/home/dilan/Private/Projects/FYP/Training Data/Gossip_lanka/"
    with open(csvpath + "aligned_GL.csv") as csvfile:
        csvReader = csv.reader(csvfile, delimiter = ",")
        for row in csvReader:
            print(row[0], row[1])
            formatFileForEmbedding("/home/dilan/Private/Projects/FYP/Training Data/Gossip_lanka/English/" + row[1].strip(), "/home/dilan/Private/Projects/FYP/Data-Formatted/gossiplanka/en/" + row[0].replace(".json", ".txt").strip(), "en")
            formatFileForEmbedding("/home/dilan/Private/Projects/FYP/Training Data/Gossip_lanka/Sinhala/" + row[0].strip(), "/home/dilan/Private/Projects/FYP/Data-Formatted/gossiplanka/si/" + row[0].replace(".json", ".txt").strip(), "si")

def getFromNewsfirstFolder():
    csvpath = "/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/golden_alignment_newsfirst_updated.txt"
    alignedEng = []
    alignedSin = []
    with open(csvpath) as csvfile:
        csvReader = csv.reader(csvfile, delimiter = "|")
        for row in csvReader:
            alignedEng.append(row[0].strip())
            alignedSin.append(row[2].strip())
    sinfilepath = "/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/Sinhala/"
    enfilepath = "/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/English/"

    sinfiles = os.listdir(sinfilepath)
    enfiles = os.listdir(enfilepath)
    for sinfile in sinfiles:
        if sinfile in alignedSin:
            print("yes")
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/Sinhala/" + sinfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/newsfirst/si/" + str(alignedSin.index(sinfile)) + ".txt", "si")
        else:
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/Sinhala/" + sinfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/newsfirst/si/" + sinfile.replace(".json", ".txt"), "si")
    for enfile in enfiles:
        if enfile in alignedEng:
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/English/" + enfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/newsfirst/en/" + str(alignedEng.index(enfile)) + ".txt", "en")
        else:
            formatArmyFileForEmbedding("/home/dilan/Private/Projects/FYP/Data-ToFormat/newsfirst/English/" + enfile, "/home/dilan/Private/Projects/FYP/Data-Formatted/newsfirst/en/" + enfile.replace(".json", ".txt"), "en")

# formatFiles("/home/dilan/Private/Projects/FYP/Data-ToFormat/en/", "/home/dilan/Private/Projects/FYP/Data-Formatted/en/")
# formatFiles("/home/dilan/Private/Projects/FYP/Data-ToFormat/si/", "/home/dilan/Private/Projects/FYP/Data-Formatted/si/")
###### Hiru
# getFromHiruFolder()
createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/hiru/en/", "/home/dilan/Private/Projects/FYP/Embeddings/datewise/hiru/en/", "en")
createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/hiru/si/", "/home/dilan/Private/Projects/FYP/Embeddings/datewise/hiru/si/", "si")

# readCsvGossipLanka()
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/gossiplanka/en/", "/home/dilan/Private/Projects/FYP/Embeddings/gossiplanka/en/", "en")
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/gossiplanka/si/", "/home/dilan/Private/Projects/FYP/Embeddings/gossiplanka/si/", "si")

# Wsws
# getFromWswsFolder()
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/wsws/en/", "/home/dilan/Private/Projects/FYP/Embeddings/wsws/en/", "en")
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/wsws/si/", "/home/dilan/Private/Projects/FYP/Embeddings/wsws/si/", "si")

# Wikipedia
# getFromWikipediaFolder()
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/wikipedia/en/", "/home/dilan/Private/Projects/FYP/Embeddings/wikipedia/en/", "en")
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/wikipedia/si/", "/home/dilan/Private/Projects/FYP/Embeddings/wikipedia/si/", "si")

# Army
# getFromArmyFolder()
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/army/en/", "/home/dilan/Private/Projects/FYP/Embeddings/army/en/", "en")
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/army/si/", "/home/dilan/Private/Projects/FYP/Embeddings/army/si/", "si")

# ITN
# getFromITNFolder()
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/itn/en/", "/home/dilan/Private/Projects/FYP/Embeddings/itn/en/", "en")
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/itn/si/", "/home/dilan/Private/Projects/FYP/Embeddings/itn/si/", "si")

# Newsfirst
# getFromNewsfirstFolder()
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/newsfirst/en/", "/home/dilan/Private/Projects/FYP/Embeddings/newsfirst/en/", "en")
# createEmbeddings("/home/dilan/Private/Projects/FYP/Data-Formatted/newsfirst/si/", "/home/dilan/Private/Projects/FYP/Embeddings/newsfirst/si/", "si")