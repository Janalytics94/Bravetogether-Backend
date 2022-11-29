import os
from datetime import date

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo

load_dotenv()
user = os.environ.get("USER")
password = os.environ.get("PASSWORD")
if user is None or password is None:
    raise RuntimeError(
        "User and password for MongoDB connection required. Could not find USER and PASSWORD environment variables."
    )

app = Flask(__name__)

cors = CORS(app, resources={r"/UserSurveys/*": {"origins": "*"}})
app.config["MONGO_DBNAME"] = "AgainstSexualHarassment"
app.config["MONGO_URI"] = (
    "mongodb+srv://"
    + user
    + ":"
    + password
    + "@againstsexualharrassmen.kc68g.mongodb.net/AgainstSexualHarassment?retryWrites=true&w=majority"
)


mongo = PyMongo(app)


# Get them all
@app.route("/UserSurveys", methods=["GET"])
def get_all_user_surveys():
    UserSurveys = mongo.db.UserSurveys
    output = []
    for u in UserSurveys.find():
        output.append(
            {
                "sex": u["sex"],
                "age": u["age"],
                "when": u["when"],
                "where": u["where"],
                "what": u["what"],
                "reported": u["reported"],
                "feelings": u["feelings"],
            }
        )
    return jsonify({"result": output})


# Get one
@app.route("/UserSuveys/search/<_id>", methods=["GET"])
def get_one_user_survey():
    UserSurveys = mongo.db.UserSurveys
    output = []
    for u in UserSurveys.find():
        output.append({"_id": u["_id"]})
    return jsonify({"result": output})


@app.route("/UserSurveys/add", methods=["POST"])
def add_experience():
    UserSurveys = mongo.db.UserSurveys

    # Personal Information
    # _id = request.json['_id']  # Automaticly generated?
    sex = request.json["sex"]  # Selection
    age = request.json["age"]

    # When
    when = request.json["when"]

    # Where
    where = request.json["where"]  # Bus, Tram, Straße, Park, Wald etc.
    address = request.json["address"]

    # What
    what = request.json["what"]  # Selection
    circumstances = request.json["circumstances"]

    # Was the Incident reported ?
    reported = request.json["reported"]

    # How did you feel ?
    feelings = request.json["feelings"]  # Freitext

    insert_date = date.today()
    insert_date = insert_date.strftime("%d/%m/%Y")

    # Alle Felder sollen die frei bleiben können, wenn jemand einfach keine genauen Angaben mehr machen kann.
    UserSurveys.insert_one(
        {
            "sex": sex,  # Selection
            "age": age,
            "when": when,
            "where": where,
            "address": address,
            "what": what,
            "circumstances": circumstances,
            "reported": reported,
            "feelings": feelings,
            "insert_date": insert_date,
        }
    )
    output = {
        "sex": sex,
        "age": age,
        "when": when,
        "where": where,
        "what": what,
        "reported": reported,
        "feelings": feelings,
        "insert_date": insert_date,
    }
    return jsonify({"result": output})


if __name__ == "__main__":
    app.run(debug=False, port=os.environ.get("PORT", 5000))
