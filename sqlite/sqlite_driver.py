from csv import reader
import sqlite3

from backend.exceptions import DatabaseUnavailableError, InvalidInputError, InvalidQueryError

EVENT_FIELDS = ["event_id", "event_title", "event_description"]
MATCH_FIELDS = ["match_id", "match_date", "match_start_time", "match_end_time",
                "match_season", "team_a_id", "team_b_id", "team_a_points", "team_b_points"]
SEASON_FIELDS = ["season_id", "season_title", "season_start_date", "season_end_date"]
TEAM_FIELDS = ["team_id", "team_name"]

class SqliteContext:
    def __init__(self, dbpath : str) -> None:
        self.dbpath = dbpath
    
    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.dbpath)
            if not self.conn:
                raise DatabaseUnavailableError("Unable to connect to db, check connection")
            self.cursor = self.conn.cursor()
            return [self.conn, self.cursor]
        except sqlite3.Error as error:
            raise DatabaseUnavailableError(f"Unable to connect to db, error: {error}")
    
    def __exit__(self, type, value, traceback):
        self.cursor.close()
        self.conn.close()

class SqliteDriver:
    def __init__(self, dbpath : str) -> None:
        self.dbpath = dbpath
    
    def create_tables(self, script_path : str):
        with SqliteContext(self.dbpath) as [conn, cur]:
            with open(script_path) as create_script:
                cur.executescript(create_script.read())
            conn.commit()
        
    def insert_from_csv(self, table : str, filepath : str, delimiter : str):
        try:
            with SqliteContext(self.dbpath) as [conn, cur]:
                with open(filepath, encoding="utf-8") as csv_file:
                    content = reader(csv_file, delimiter=delimiter)
                    header = next(content)

                    for row in content:
                        cur.execute(
                            f"INSERT OR REPLACE INTO {table} ({','.join(header)}) VALUES ({','.join(row)});"
                        )
                    conn.commit()
        except sqlite3.Error as error:
            raise InvalidQueryError(f"Sqlite error while adding data from file {filepath} : {error}")
    
    def add_mock_data(self, data_directory : str):
        self.insert_from_csv("Seasons", f"{data_directory}/seasons.csv", ";")
        self.insert_from_csv("Teams", f"{data_directory}/teams.csv", ";")
        self.insert_from_csv("Matches", f"{data_directory}/matches.csv", ";")
        self.insert_from_csv("Events", f"{data_directory}/events.csv", ";")
    
    def get_insert_query(self, table : str, data : dict):
        insert_query = f"INSERT INTO {table} ("
        for key in data:
            insert_query += f"{key}, "
        insert_query = insert_query[:-2] + ") VALUES ("
        for value in data.values():
            insert_query += f"'{value}', " if type(value) == str else f"{value}, "
        insert_query = insert_query[:-2] + ")"
        return insert_query
    
    def get_update_query(self, table : str, data : dict, target_name : str, target_value):
        update_query = f"UPDATE {table} SET "
        for key in data:
            update_query += f"{key} = "
            update_query += f"'{data[key]}', " if type(data[key]) == str else f"{data[key]}, "
        update_query = update_query[:-2] + f" WHERE {target_name} = {target_value}"
        return update_query
    
    def input_valid(self, allowed_fields : list, input_data : dict):
        for key in input_data:
            if key not in allowed_fields:
                raise InvalidInputError(f"Illegal field in input data: {key}")
        return True

    def get_events(self):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute("SELECT event_id, event_title, event_description FROM Events")
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching events: {error}")
            rows = [
                {
                    "event_id": entry[0],
                    "event_title": entry[1],
                    "event_description": entry[2]
                } for entry in cur.fetchall()
            ]
        return rows

    def add_event(self, event_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(EVENT_FIELDS, event_data):
                try:
                    cur.execute(self.get_insert_query("Events", event_data))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while adding event: {error}")
                return True 
        return False

    def edit_event(self, event_id : int, event_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(EVENT_FIELDS, event_data):
                if "event_id" in event_data:
                    del event_data["event_id"]
                try:
                    cur.execute(self.get_update_query("Events", event_data, "event_id", event_id))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while editing event: {error}")
                return True
        return False
    
    def delete_event(self, event_id : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"DELETE FROM Events WHERE event_id = {event_id}")
                conn.commit()
                return True
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while deleting event: {error}")

    def get_seasons(self):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute("SELECT * FROM Seasons")
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching seasons: {error}")
            rows = [
                {
                    "season_id": entry[0],
                    "season_title": entry[1],
                    "season_start_date": entry[2],
                    "season_end_date": entry[3]
                } for entry in cur.fetchall()
            ]
        return rows

    def add_season(self, season_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(SEASON_FIELDS, season_data):
                try:
                    cur.execute(self.get_insert_query("Seasons", season_data))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while adding new season: {error}")
                return True
        return False

    def edit_season(self, season_id, season_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(SEASON_FIELDS, season_data):
                if "season_id" in season_data:
                    del season_data["season_id"]
                try:
                    cur.execute(self.get_update_query("Seasons", season_data, "season_id", season_id))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while editing season: {error}")
                return True
        return False
    
    def delete_season(self, season_id):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"DELETE FROM Seasons WHERE season_id = {season_id}")
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while deleting season: {error}")
            return True

    def get_season_highscore(self, season_id : int):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute((f"SELECT team_id, team_name, SUM(points) AS highscore FROM ("
                            f"SELECT t.team_id AS team_id, t.team_name as team_name, m.team_a_points as points "
                            f"FROM Matches m, Teams t WHERE m.match_season = {season_id} AND t.team_id = m.team_a_id"
                            f" UNION ALL "
                            f"SELECT t.team_id AS team_id, t.team_name as team_name, m.team_b_points as points "
                            f"FROM Matches m, Teams t WHERE m.match_season = {season_id} AND t.team_id = m.team_b_id"
                            f") GROUP BY team_name ORDER BY highscore DESC"))
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while getting season highscore: {error}")
            rows = [{"team_id": entry[0], "team_name": entry[1], "team_score": entry[2]} for entry in cur.fetchall()]
        return rows

    def get_teams(self):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute("SELECT team_id, team_name FROM Teams")
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while getting teams: {error}")
            rows = [
                {
                    "team_id": entry[0],
                    "team_name": entry[1]
                } for entry in cur.fetchall()
            ]
        return rows
    
    def add_team(self, team_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(TEAM_FIELDS, team_data):
                try:
                    cur.execute(self.get_insert_query("Teams", team_data))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while adding new team: {error}")
                return True
        return False
    
    def edit_team(self, team_id : int, team_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(TEAM_FIELDS, team_data):
                if "team_id" in team_data:
                    del team_data["team_id"]
                try:
                    cur.execute(self.get_update_query("Teams", team_data, "team_id", team_id))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while editing team: {error}")
                return True
        return False
    
    def delete_team(self, team_id : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"DELETE FROM Teams WHERE team_id = {team_id}")
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while deleting team: {error}")
            return True

    def get_matches(self):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute("SELECT * FROM Matches")
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while getting matches: {error}")
            rows = [
                {
                    "match_id": entry[0],
                    "match_date": entry[1],
                    "match_start_time": entry[2],
                    "match_end_time": entry[3],
                    "match_season": entry[4],
                    "team_a_id": entry[5],
                    "team_b_id": entry[6],
                    "team_a_points": entry[7],
                    "team_b_points": entry[8]
                } for entry in cur.fetchall()
            ]
        return rows

    def get_match(self, match_id : int):
        result = {}
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"SELECT " 
                            f"m.match_id, m.match_date, m.match_start_time, m.match_end_time, t1.team_name,"
                            f"t2.team_name, m.team_a_points, m.team_b_points "
                            f"FROM Matches m, Teams t1, Teams t2 "
                            f"WHERE m.match_id = {match_id} AND m.team_a_id = t1.team_id AND m.team_b_id = t2.team_id")
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while getting a match: {error}")
            row = cur.fetchall()
            if len(row) > 0:
                result = {
                    "match_id": row[0][0],
                    "match_date": row[0][1],
                    "match_start_time": row[0][2],
                    "match_end_time": row[0][3],
                    "team_a_name": row[0][4],
                    "team_b_name": row[0][5],
                    "team_a_points": row[0][6],
                    "team_b_points": row[0][7]
                    }
        return result

    def get_season_matches(self, season_id : int):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"SELECT " 
                            f"m.match_id, m.match_date, m.match_start_time, m.match_end_time, t1.team_name,"
                            f"t2.team_name, m.team_a_points, m.team_b_points "
                            f"FROM Matches m, Teams t1, Teams t2 "
                            f"WHERE m.match_season = {season_id} AND m.team_a_id = t1.team_id "
                            f"AND m.team_b_id = t2.team_id")
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while getting season matches: {error}")
            rows = [{
                "match_id": entry[0],
                "match_date": entry[1],
                "match_start_time": entry[2],
                "match_end_time": entry[3],
                "team_a_name": entry[4],
                "team_b_name": entry[5],
                "team_a_points": entry[6],
                "team_b_points": entry[7]} for entry in cur.fetchall()]
        return rows

    def add_match(self, season_id : int, match_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(MATCH_FIELDS, match_data):
                match_data["match_season"] = season_id
                try:
                    cur.execute(self.get_insert_query("Matches", match_data))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while adding new match: {error}")
                return True
        return False
    
    def edit_match(self, match_id : int, match_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(MATCH_FIELDS, match_data):
                if "match_id" in match_data:
                    del match_data["match_id"]
                try:
                    cur.execute(self.get_update_query("Matches", match_data, "match_id", match_id))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while editing match: {error}")
                return True
        return False
    
    def delete_match(self, match_id : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"DELETE FROM Matches WHERE match_id = {match_id}")
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while deleting match: {error}")
            return True
