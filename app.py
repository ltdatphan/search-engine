import flask
from flask import request, jsonify, render_template
import pickle
from pathlib import Path
from BM25_custom import BM25OkapiCustom
from helper import tokenize, remove_stopword
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app, resources={r"/search": {"origins": "https://inquisitive-bunny-f80acf.netlify.app/"}, r"/": {"origins": "*"}})

filehandler = open(Path("./trained_models/bm25_model.obj"), "rb")
bm25_model = pickle.load(filehandler)
filehandler = open(Path("./trained_models/nb_model.obj"), "rb")
nb_model = pickle.load(filehandler)


@app.route("/", methods=["GET"])
def home():
    return """<h1>API for CPS842</h1>"""


@app.route("/search", methods=["GET"])
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


# if __name__ == "__main__":
#     # filehandler = open(Path("./trained_models/bm25_model.obj"), "rb")
#     # bm25_model = pickle.load(filehandler)
#     # filehandler = open(Path("./trained_models/nb_model.obj"), "rb")
#     # nb_model = pickle.load(filehandler)
#     app.run()
