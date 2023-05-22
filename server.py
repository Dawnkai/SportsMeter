from flask import jsonify, Flask, request
from flask_jwt_extended import create_access_token, JWTManager

from sqlite.sqlite_driver import SqliteDriver

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
db = SqliteDriver("database.db")

@app.before_first_request
def setup_database():
    db.create_tables()
    db.add_mock_data()

@app.route("/api/register", methods=["POST"])
def register():
    return {"response": "registered"}

@app.route("/api/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Invalid login or password."}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route("/api/seasons", methods=["GET", "PUT", "POST"])
def get_seasons():
    if request.method == "POST":
        db.add_season(request.json)
    elif request.method == "PUT":
        db.edit_season(request.json)
    return db.get_seasons()

@app.route("/api/seasons/<season_id>/matches", methods=["GET", "POST"])
def get_season_matches(season_id):
    if request.method == "POST":
        db.add_match(season_id, request.json)
    return db.get_season_matches(season_id)

@app.route("/api/seasons/<season_id>/highscore", methods=["GET"])
def get_season_highscore(season_id):
    return db.get_season_highscore(season_id)

@app.route("/api/events", methods=["GET", "PUT", "POST"])
def get_events():
    if request.method == "POST":
        db.add_event(request.json)
    elif request.method == "PUT":
        db.edit_event(request.json)
    return db.get_events()

@app.route("/api/matches/<match_id>", methods=["GET", "PUT", "DELETE"])
def get_matches(match_id):
    if request.method == "PUT":
        if db.edit_match(match_id, request.json):
            return db.get_match(match_id), 200
        return {"msg": "Unable to edit match"}, 401
    elif request.method == "DELETE":
        if db.delete_match(match_id):
            return {"msg": "Match deleted."}, 201
        return {"msg": "Unable to delete match"}, 404
    return db.get_match(match_id)
