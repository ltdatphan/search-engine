# import gzip
# from pathlib import Path
from string import punctuation
# from bs4 import BeautifulSoup
# import json
# import os
# import csv
# import random
# import requests


# def reduceCorpusSize(corpusPath, newSize):
#     count = 0
#     with gzip.open(Path(f"./data/smaller_corpus_{newSize}.jsonl.gz"), "wt") as newFile:
#         with gzip.open(Path(corpusPath), "r") as file:
#             for line in file:  # Line by line
#                 count += 1
#                 newFile.write(line.decode("utf-8"))
#                 if count == newSize:
#                     break


# def construct_wiki_corpus(
#     size=10, corpus_new_name="wiki_corpus", topics_reldocs_file_path="./data/train_topics_reldocs.tsv"
# ):
#     pathToTsvFile = Path(topics_reldocs_file_path)

#     with gzip.open(Path(f"./data/{corpus_new_name}_{size}.jsonl.gz"), "wt") as newFile:
#         with open(pathToTsvFile) as file:
#             data_file = csv.reader(file, delimiter="\t")
#             for line in data_file:
#                 label = line[1]  # label of the data
#                 data = line[2].split(",")

#                 # Extract 50 random ids from the class
#                 random_50 = random.sample(set(data), size)

#                 for id in random_50:
#                     response = requests.get(
#                         url=f"https://en.wikipedia.org/w/index.php?curid={id}",
#                     )
#                     soup = BeautifulSoup(response.content, "html.parser")

#                     title = soup.find(id="firstHeading")

#                     text_content = ""
#                     results = soup.find(id="bodyContent").find_all("p")
#                     for r in results:
#                         text_content += r.text

#                     tempDict = {"topic": label, "id": id, "title": title.text, "content": text_content}
#                     # print(json.dumps(tempDict))
#                     newFile.write(json.dumps(tempDict))
#                     newFile.write("\n")
#                     # exit()


# def extractCorpusContent(corpusPath):
#     with gzip.open(Path(corpusPath), "r") as file:
#         docCounter = 0
#         for line in file:  # Read the files line by line
#             tempDocObj = json.loads(line)  # Load the data
#             doc_content = stripHtmlTags(tempDocObj["contents"])

#             doc_content = " ".join(tokenize(doc_content))
#             writeContentToFile(
#                 "./output/content/" + str(docCounter) + "_" + str(tempDocObj["id"]) + ".txt", doc_content
#             )
#             docCounter += 1


# def readExtractedContentFromFolder(folderPath):
#     folderPath = Path(folderPath)
#     # fileList = os.listdir(folderPath)
#     fileList = sorted((f for f in os.listdir(folderPath) if not f.startswith(".")), key=str.lower)
#     # print(fileList)
#     lines = []
#     for file in fileList:
#         # if file.startswith("."):

#         #     continue

#         f = open(folderPath / file, "r", encoding="utf8", errors="ignore")
#         # append each line in the file to a list
#         lines.append((" ").join(f.readlines()))
#         # print(f.readlines())
#         f.close()

#     return fileList, lines


# def retrieveRelatedDocIds(topic, filePath):
#     # pathToTopicKeyWordsFile = Path("./data/train_topics_keywords.tsv")

#     with open(Path(filePath)) as file:
#         tsv_file = csv.reader(file, delimiter="\t")
#         for line in tsv_file:
#             topics_list.append(line[1])
#             topics_keywords_list.append(line[2])


# def stripHtmlTags(content):
#     soup = BeautifulSoup(content, "html.parser")
#     return soup.get_text(separator=" ")


def tokenize(line):
    # Remove non-ASCII chars
    line = "".join([c if ord(c) < 128 else " " for c in line])

    # Remove possessives
    line = line.replace("'s", "")

    # Remove special characters
    special_chars = '!@#$%^&*()[]\{\}<>?`~\\|;:"/'
    for c in special_chars:
        line = line.replace(c, "")

    # Convert all case to lower case and start tokenization
    lineArr = line.lower().split()

    # Strip leading and trailing punctuations from each token
    lineArr = [token.strip(punctuation) for token in lineArr]

    while "" in lineArr:
        lineArr.remove("")

    return lineArr


# def openStopWordsFile(filepath: str):
#     stopwordsFile = open('stopwords.txt', 'r')
#     stopwords = dict.fromkeys(stopwordsFile.read().splitlines())
#     stopwordsFile.close()

#     return stopwords


def remove_stopword(list_of_words):
    stopwordsFile = open(Path("stopwords.txt"), "r")
    stopwords = dict.fromkeys(stopwordsFile.read().splitlines())
    stopwordsFile.close()

    res = []

    for w in list_of_words:
        if w not in stopwords:
            res.append(w)
    return res


# def writeContentToFile(filePath, fileContent):
#     with open(Path(filePath), "w") as write_file:
#         write_file.write(fileContent)
#         write_file.close()
