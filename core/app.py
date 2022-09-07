from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from werkzeug.exceptions import InternalServerError, NotFound, BadRequest
from bson import json_util, ObjectId
import json

app = Flask(__name__)

conn_str = "mongodb+srv://josh:josh@cluster0.sl3j8fb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str, tls=True, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)

try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the database server.")

CORS(app)

db = client["futureproof-test"]
test1 = db["test1"]

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/cats", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        all_cats = list(test1.find())   
        print(all_cats)
        # return json.loads(json_util.dumps(all_cats))
        return json_util.dumps(all_cats)
    elif request.method == "POST":
        data = request.json
        test1.insert_one(data)
        return f"{data['name']} has been created", 201

@app.route("/cats/<string:id>", )
def show(id):
    try:        
        return json_util.dumps(test1.find_one(ObjectId(id)))
    except:
        raise BadRequest("We don't have this cat")

@app.route("/cats/<string:id>", )
def show(id):
    try:        
        return json_util.dumps(test1.find_one(ObjectId(id)))
    except:
        raise BadRequest("We don't have this cat")

@app.errorhandler(NotFound)
def handle_404(err):
    return jsonify({"message": f"Oops {err}"}), 404

@app.errorhandler(InternalServerError)
def handle_500(err):
    return jsonify({"message": f"It is ont you, it is me"}), 500

if __name__ == "__main__":
    app.run()
