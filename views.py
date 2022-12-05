from flask import Blueprint, render_template, request, jsonify

views = Blueprint(__name__, "views")


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/query")
def query():
    return render_template("index.html", name="hello")


@views.route("/profile")
def profile():
    args = request.args
    name = args.get("name")
    return render_template("index.html", name=name)


@views.route("/json")
def get_json():
    return jsonify({"name": "david"})


@views.route("/predict", methods=["POST"])
def predict():
    data = request.form
    name = data.get("name")
    # query_df = pd.DataFrame(json_)
    # query = pd.get_dummies(query_df)
    # prediction = clf.predict(query)
    print(name)
    return jsonify({"prediction": name})
