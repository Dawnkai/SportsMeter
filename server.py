from flask import jsonify, Flask, request
from flask_jwt_extended import create_access_token, JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

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

@app.route("/api/seasons", methods=["GET"])
def get_seasons():
    return [{"id": 0, "title": "Season 1"}, {"id": 1, "title": "Season 2"}, {"id": 2, "title": "Season 3"}]

@app.route("/api/seasons/<season_id>/matches", methods=["GET"])
def get_season_matches(season_id):
    if int(season_id) == 0:
        return [{"title": "Match 1 (Season 1)", "id": 0}, {"title": "Match 2 (Season 1)", "id": 1}]
    elif int(season_id) == 1:
        return [{"title": "Match 1 (Season 2)", "id": 2}]
    elif int(season_id) == 2:
        return [{"title": "Match 1 (Season 3)", "id": 3}, {"title": "Match 2 (Season 3)", "id": 4}, {"title": "Match 3 (Season 3)", "id": 5}]
    return []

@app.route("/api/seasons/<season_id>/highscore", methods=["GET"])
def get_season_highscore(season_id):
    if int(season_id) == 0:
        return [
            {"team_id": 0, "team_name": "Team 1", "team_score": 2000},
            {"team_id": 2, "team_name": "Team 3", "team_score": 1000},
            {"team_id": 1, "team_name": "Team 2", "team_score": 500}
        ]
    elif int(season_id) == 1:
        return [
            {"team_id": 1, "team_name": "Team 2", "team_score": 100},
            {"team_id": 0, "team_name": "Team 1", "team_score": 50}
        ]
    elif int(season_id) == 2:
        return [
            {"team_id": 2, "team_name": "Team 3", "team_score": 5000},
            {"team_id": 0, "team_name": "Team 1", "team_score": 1000},
            {"team_id": 3, "team_name": "Team 4", "team_score": 100},
            {"team_id": 1, "team_name": "Team 2", "team_score": 50}
        ]
    return []
