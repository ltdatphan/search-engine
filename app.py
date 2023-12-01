import flask
from flask import request, jsonify, render_template
import pickle
from pathlib import Path
from BM25_custom import BM25OkapiCustom
from helper import tokenize, remove_stopword
from flask_cors import cross_origin
import bz2file as bz2
from pathlib import Path

app = flask.Flask(__name__)
app.config["DEBUG"] = True
# CORS(app, resources={r"/search": {"origins": "https://inquisitive-bunny-f80acf.netlify.app/"}, r"/": {"origins": "*"}})

# filehandler = open(Path("./trained_models/bm25_model.obj"), "rb")
# bm25_model = pickle.load(filehandler)
# filehandler = open(Path("./trained_models/nb_model.obj"), "rb")
# nb_model = pickle.load(filehandler)

# Reading the compressed model
# compressed_bm25_model = bz2.BZ2File("./trained_models/compressed_bm25_model.pbz2", "rb")
# bm25_model = pickle.load(compressed_bm25_model)
# compressed_nb_model = bz2.BZ2File("./trained_models/compressed_nb_model.pbz2", "rb")
# nb_model = pickle.load(compressed_nb_model)

# Smaller models
filehandler = open(Path("./trained_models/bm25_model.obj"), "rb")
bm25_model = pickle.load(filehandler)
filehandler = open(Path("./trained_models/nb_model.obj"), "rb")
nb_model = pickle.load(filehandler)


@app.route("/", methods=["GET"])
def home():
    return """<h1>API for CPS842</h1>"""


@app.route("/search", methods=["GET"])
@cross_origin(origins=["https://search-engine-cps842.netlify.app/"])
def search():
    query = request.args["query"]

    # Preprocessing
    userInput = " ".join(remove_stopword(tokenize(query)))

    # Get the probability for each category
    res = nb_model.predict_proba([userInput])

    # Get the top 5 most relevant categories and their scores
    relevant_topics_list = sorted(zip(nb_model.classes_, res[0]), key=lambda x: x[1], reverse=True)[:5]

    # Only extract the text of the 5 most relevant categories
    relevant_topics = []
    for topic in relevant_topics_list:
        relevant_topics.append(topic[0])

    tokenized_query = userInput.split(" ")

    # Get the 10 most relevant documents
    results = bm25_model.get_highest_relevant_k_scores(tokenized_query, relevant_topics, 10)

    return jsonify({"query": query, "result": results})


@app.route("/search_scores", methods=["GET"])
@cross_origin(origins=["https://inquisitive-bunny-f80acf.netlify.app", "http://localhost:3000"])
def search_scores():
    query = request.args["query"]

    # Preprocessing
    userInput = " ".join(remove_stopword(tokenize(query)))

    # Get the probability for each category
    res = nb_model.predict_proba([userInput])

    # Get the top 5 most relevant categories and their scores
    relevant_topics_list = sorted(zip(nb_model.classes_, res[0]), key=lambda x: x[1], reverse=True)[:5]

    # Only extract the text of the 5 most relevant categories
    relevant_topics = []
    for topic in relevant_topics_list:
        relevant_topics.append(topic[0])

    tokenized_query = userInput.split(" ")

    # Get the 10 most relevant documents
    results = bm25_model.get_highest_relevant_k_scores(tokenized_query, relevant_topics, 10)

    # Get 10 best topics from Naive Bayes
    top_10_nb_scores = sorted(zip(nb_model.classes_, res[0]), key=lambda x: x[1], reverse=True)[:10]

    return jsonify({"query": query, "result": results, "nb_result": top_10_nb_scores})
