from flask import jsonify, Flask, request
from flask_jwt_extended import create_access_token, JWTManager

from sqlite.sqlite_driver import SqliteDriver
from backend.exceptions import DatabaseUnavailableError, InvalidInputError, InvalidQueryError

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
db = SqliteDriver("database.db")

def throws_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DatabaseUnavailableError:
            return jsonify({"msg": "Database unavailable."}), 500
        except InvalidInputError as err:
            return jsonify({"msg": err}), 401
        except InvalidQueryError:
            return jsonify({"msg": "Backend error. Check logs."}), 503
    return wrapper

@throws_exception
@app.before_first_request
def setup_database():
    db.create_tables("sqlite/create.sql")
    db.add_mock_data("mock_data")

@throws_exception
@app.route("/api/register", methods=["POST"])
def register():
    return {"response": "registered"}

@throws_exception
@app.route("/api/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Invalid login or password."}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@throws_exception
@app.route("/api/seasons", methods=["GET", "POST"])
def seasons():
    if request.method == "POST":
        db.add_season(request.json)
    return db.get_seasons()

@throws_exception
@app.route("/api/season/<season_id>", methods=["PUT", "DELETE"])
def season(season_id):
    if request.method == "PUT":
        db.edit_season(season_id, request.json)
        return db.get_seasons()
    db.delete_season(season_id)
    return jsonify({"msg": "Season deleted."}), 204

@throws_exception
@app.route("/api/seasons/<season_id>/matches", methods=["GET", "POST"])
def season_matches(season_id):
    if request.method == "POST":
        db.add_match(season_id, request.json)
    return db.get_season_matches(season_id)

@throws_exception
@app.route("/api/seasons/<season_id>/highscore", methods=["GET"])
def season_highscore(season_id):
    return db.get_season_highscore(season_id)

@throws_exception
@app.route("/api/events", methods=["GET", "POST"])
def events():
    if request.method == "POST":
        db.add_event(request.json)
    return db.get_events()

@throws_exception
@app.route("/api/events/<event_id>", methods=["PUT", "DELETE"])
def event(event_id):
    if request.method == "PUT":
        db.edit_event(event_id, request.json)
        return db.get_events()
    db.delete_event(event_id)
    return jsonify({"msg": "Event deleted"}), 204

@throws_exception
@app.route("/api/matches/", methods=["GET"])
def matches():
    return db.get_matches()

@throws_exception
@app.route("/api/matches/<match_id>", methods=["GET", "PUT", "DELETE"])
def match(match_id):
    if request.method == "PUT":
        if db.edit_match(match_id, request.json):
            return db.get_match(match_id), 200
        return {"msg": "Unable to edit match"}, 401
    elif request.method == "DELETE":
        if db.delete_match(match_id):
            return {"msg": "Match deleted."}, 201
        return {"msg": "Unable to delete match"}, 404
    return db.get_match(match_id)

@throws_exception
@app.route("/api/teams/", methods=["GET", "POST"])
def teams():
    if request.method == "POST":
        db.add_team(request.json)
    return db.get_teams()

@throws_exception
@app.route("/api/teams/<team_id>", methods=["PUT", "DELETE"])
def team(team_id):
    if request.method == "PUT":
        db.edit_team(team_id, request.json)
        return db.get_teams()
    db.delete_team(team_id)
    return jsonify({"msg": "Team deleted."}), 204
