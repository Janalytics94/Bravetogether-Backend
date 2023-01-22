import os
from datetime import date

from dotenv import load_dotenv


from chalice import Chalice
from pymongo import MongoClient

load_dotenv()
user = os.environ.get("USER")
password = os.environ.get("PASSWORD")
host = os.environ.get("HOST")
if user is None or password is None:
    raise RuntimeError(
        "User and password for MongoDB connection required. Could not find USER, PASSWORD and HOST environment variables."
    )

app = Chalice(app_name="bravetogether-backend")
app.api.cors = True


mongo = MongoClient(f"mongodb+srv://{user}:{password}@{host}/AgainstSexualHarassment?retryWrites=true&w=majority")
db = mongo.AgainstSexualHarassment

# Get them all
@app.route("/UserSurveys", methods=["GET"])
def get_all_user_surveys():
    UserSurveys = db.UserSurveys
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
    return {"result": output}


# Get one
@app.route("/UserSuveys/search/{id}", methods=["GET"])
def get_one_user_survey(id):
    UserSurveys = db.UserSurveys
    output = []
    for u in UserSurveys.find():
        output.append({"_id": u["_id"]})
    return {"result": output}


@app.route("/UserSurveys/add", methods=["POST"])
def add_experience():
    UserSurveys = db.UserSurveys
    request = app.current_request
    print(request.to_dict())
    print(request.raw_body)
    print(request.json_body)

    # Personal Information
    sex = request.json_body["sex"]  # Selection
    age = request.json_body["age"]

    # When
    when = request.json_body["when"]

    # Where
    where = request.json_body["where"]  # Bus, Tram, Straße, Park, Wald etc.
    address = request.json_body["address"]

    # What
    what = request.json_body["what"]  # Selection
    circumstances = request.json_body["circumstances"]

    # Was the Incident reported ?
    reported = request.json_body["reported"]

    # How did you feel ?
    feelings = request.json_body["feelings"]  # Freitext

    insert_date = date.today()
    insert_date = insert_date.strftime("%d/%m/%Y")

    # Alle Felder sollen die frei bleiben können, wenn jemand einfach keine genauen Angaben mehr machen kann.
    insert_result = UserSurveys.insert_one(
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
        "_id": str(insert_result.inserted_id),
        "sex": sex,
        "age": age,
        "when": when,
        "where": where,
        "what": what,
        "reported": reported,
        "feelings": feelings,
        "insert_date": insert_date,
    }
    return {"result": output}
