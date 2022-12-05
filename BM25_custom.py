import math
import numpy as np

# from multiprocessing import Pool, cpu_count
# from pathlib import Path
# import json


class BM25OkapiCustom:
    def __init__(self, k1=1.5, b=0.75, epsilon=0.25):
        self.corpus_size = 0  # Number of documents
        self.avrg_doc_len = 0  # Average length of document
        self.doc_freqs_list = []  # Term frequency of each document
        self.idf = {}
        self.doc_len_list = []  # List of document lengths
        self.sum_doc_len = 0  # Total number of terms in corpus (sum of all document length)

        # Parameters for Okapi BM25
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon

        # Dict to store term frequency of entire collection
        self.tf_of_collection = {}

        # Keep track of other info for each doc we add
        self.doc_title_list = []
        self.doc_id_list = []
        self.doc_category_list = []

    # Add a new document to the index, and update the variables
    def addDoc(self, doc_title, doc_id, doc_category, tokenized_doc_content):
        # Store the info of current doc
        self.doc_title_list.append(doc_title)
        self.doc_id_list.append(doc_id)
        self.doc_category_list.append(doc_category)

        # Update
        self.doc_len_list.append(len(tokenized_doc_content))
        self.sum_doc_len += len(tokenized_doc_content)
        self.corpus_size += 1

        freq = {}  # keep track of word frequencies in current doc
        for word in tokenized_doc_content:
            if word not in freq:
                freq[word] = 1
            else:
                freq[word] += 1
        self.doc_freqs_list.append(freq)  # Add tf of curr doc

        # Update the tf of the collection
        for word, tf in freq.items():
            try:
                self.tf_of_collection[word] += 1
            except KeyError:
                self.tf_of_collection[word] = 1

        # Update avrg document length
        self.avrg_doc_len = self.sum_doc_len / self.corpus_size

    # idf calculation
    def calculate_idf(self):
        sum_of_idf = 0
        negative_idf_list = []

        for term, tf in self.tf_of_collection.items():
            idf = math.log(self.corpus_size - tf + 0.5) - math.log(tf + 0.5)
            self.idf[term] = idf
            sum_of_idf = sum_of_idf + idf

            if idf < 0:
                negative_idf_list.append(term)

        self.avg_if = sum_of_idf / len(self.idf)

        calc_epsilon = self.epsilon / len(self.idf)

        for term in negative_idf_list:
            self.idf[term] = calc_epsilon

    # calculate scores of terms in query
    def calc_scores(self, query):
        doc_len_list = np.array(self.doc_len_list)
        score_list = np.zeros(self.corpus_size)

        # Go through each term in the query
        for term in query:

            query_term_freq = []
            for doc_freq in self.doc_freqs_list:
                if term in doc_freq:
                    query_term_freq.append(doc_freq.get(term))
                else:
                    query_term_freq.append(0)

            term_freq_np = np.array(query_term_freq)

            score_list += (self.idf.get(term) or 0) * (
                term_freq_np
                * (self.k1 + 1)
                / (term_freq_np + self.k1 * (1 - self.b + self.b * doc_len_list / self.avrg_doc_len))
            )

        # All of the lists in this class is stored based on insertion order
        result = []
        for i, score in enumerate(score_list):
            tempDict = {
                "id": self.doc_id_list[i],
                "title": self.doc_title_list[i],
                "topic": self.doc_category_list[i],
                "score": score,
            }
            result.append(tempDict)

        return result

        # return score_list

    def calc_scores_relevant_topics(self, query, relevant_topics):
        doc_len_list = np.array(self.doc_len_list)
        score_list = np.zeros(self.corpus_size)

        # Go through each term in the query
        for term in query:

            query_term_freq = []
            for doc_freq in self.doc_freqs_list:
                if term in doc_freq:
                    query_term_freq.append(doc_freq.get(term))
                else:
                    query_term_freq.append(0)

            term_freq_np = np.array(query_term_freq)

            score_list += (self.idf.get(term) or 0) * (
                term_freq_np
                * (self.k1 + 1)
                / (term_freq_np + self.k1 * (1 - self.b + self.b * doc_len_list / self.avrg_doc_len))
            )

        # All of the lists in this class is stored based on insertion order
        result = []
        for i, score in enumerate(score_list):
            if self.doc_category_list[i] in relevant_topics:
                tempDict = {
                    "id": self.doc_id_list[i],
                    "title": self.doc_title_list[i],
                    "topic": self.doc_category_list[i],
                    "score": score,
                }
                result.append(tempDict)

        return result

        # return score_list

    # return highest scores (by default return 10 highest scores)
    def get_highest_k_scores(self, query, k=10):
        scores = self.calc_scores(query)

        if k > len(scores):
            k = len(scores)

        sortedScores = sorted(scores, key=lambda d: d["score"], reverse=True)

        return sortedScores[:k]

    # return highest scores (by default return 10 highest scores)
    def get_highest_relevant_k_scores(self, query, relevant_topics, k=10):
        scores = self.calc_scores_relevant_topics(query, relevant_topics)

        if k > len(scores):
            k = len(scores)

        sortedScores = sorted(scores, key=lambda d: d["score"], reverse=True)

        return sortedScores[:k]
