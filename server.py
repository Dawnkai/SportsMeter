from flask import jsonify, Flask, request
from flask_jwt_extended import create_access_token, JWTManager

from sqlite.sqlite_driver import SqliteDriver
from backend.exceptions import DatabaseUnavailableError, InvalidInputError, InvalidQueryError, NoResultError

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
db = SqliteDriver("database.db")

def throws_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DatabaseUnavailableError as err:
            print(err)
            return jsonify({"msg": "Database unavailable."}), 500
        except InvalidInputError as err:
            return jsonify({"msg": err}), 401
        except InvalidQueryError as err:
            print(err)
            return jsonify({"msg": "Backend error. Check logs."}), 503
        except NoResultError as err:
            return jsonify({"msg": err}), 404
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
@app.route("/api/notifications", methods=["GET", "POST"])
def notifications():
    if request.method == "POST":
        db.add_notifiaction(request.json)
    return db.get_notifiactions()

@throws_exception
@app.route("/api/notifications/<notification_id>", methods=["PUT", "DELETE"])
def notification(notification_id):
    if request.method == "PUT":
        db.edit_notifiaction(notification_id, request.json)
        return db.get_notifiactions()
    db.delete_notifiaction(notification_id)
    return jsonify({"msg": "Notifiaction deleted"}), 204

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
@app.route("/api/matches/<match_id>/players", methods=["GET", "POST"])
def match_players(match_id):
    if request.mathod == "POST":
        if "player_id" not in request.json:
            raise InvalidInputError("Player ID not provided.")
        db.add_match_player(match_id, request.json["player_id"])
    return db.get_match_players(match_id)

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

@app.route("/api/substitutions", methods=["GET", "POST"])
def substitutions():
    if request.method == "POST":
        db.add_substitution(request.json)
    return db.get_substitutions()

@app.route("/api/substitutions/<substitution_id>", methods=["GET", "PUT"])
def substitution(substitution_id):
    if request.method == "PUT":
        db.edit_substitution(substitution_id, request.json)
    return db.get_substitution(substitution_id, request.json), 200

@app.route("/api/players", methods=["GET", "POST"])
def players():
    if request.method == "POST":
        db.add_player(request.json)
    return db.get_players()

@app.route("/api/players/<player_id>", methods=["GET", "PUT", "DELETE"])
def player(player_id):
    if request.method == "DELETE":
        db.delete_player(player_id)
        return jsonify({"msg": "Player deleted."})
    if request.method == "PUT":
        db.edit_player(player_id, request.json)
    return db.get_player(player_id)
