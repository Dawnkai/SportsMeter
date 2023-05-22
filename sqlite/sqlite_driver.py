from csv import reader
import sqlite3

class SqliteDriver:
    def __init__(self, dbpath : str) -> None:
        self.dbpath = dbpath

    def get_handle(self):
        conn = None
        try:
            conn = sqlite3.connect(self.dbpath, check_same_thread=False)
        except sqlite3.Error as error:
            print(f"Sqlite error in get_connection: {error}")
        return [conn, conn.cursor()]
    
    def create_tables(self, script_path : str):
        conn, cur = self.get_handle()
        if conn:
            with open(script_path) as create_script:
                cur.executescript(create_script.read())
            conn.commit()
            cur.close()
            conn.close()
        
    def insert_from_csv(self, table : str, filepath : str, delimiter : str):
        conn, cur = self.get_handle()
        if conn:
            try:
                with open(filepath, encoding="utf-8") as csv_file:
                    content = reader(csv_file, delimiter=delimiter)
                    header = next(content)

                    for row in content:
                        cur.execute(
                            f"INSERT OR REPLACE INTO {table} ({','.join(header)}) VALUES ({','.join(row)});"
                        )
                conn.commit()
            except sqlite3.Error as error:
                print(f"Sqlite error while adding data from file {filepath} : {error}")
    
    def add_mock_data(self, data_directory : str):
        self.insert_from_csv("Seasons", f"{data_directory}/seasons.csv", ";")
        self.insert_from_csv("Teams", f"{data_directory}/teams.csv", ";")
        self.insert_from_csv("Matches", f"{data_directory}/matches.csv", ";")
        self.insert_from_csv("Events", f"{data_directory}/events.csv", ";")

    def event_input_valid(self, event_input : dict):
        allowed_fields = ["event_id", "event_title", "event_description"]
        for key in event_input.keys():
            if key not in allowed_fields:
                return False
        return True

    def get_events(self):
        conn, cur = self.get_handle()
        rows = []
        if conn:
            cur.execute("SELECT event_id, event_title, event_description FROM Events")
            rows = [
                {
                    "event_id": entry[0],
                    "event_title": entry[1],
                    "event_description": entry[2]
                } for entry in cur.fetchall()
            ]
            cur.close()
            conn.close()
        return rows

    def add_event(self, event_data : dict):
        conn, cur = self.get_handle()
        if conn and self.event_input_valid(event_data):
            insert_query = "INSERT INTO Events ("
            for key in event_data.keys():
                insert_query += f"{key}, "
            insert_query = insert_query[:-2] + ") VALUES ("
            for value in event_data.values():
                if type(value) == str:
                    insert_query += f"'{value}', "
                else:
                    insert_query += f"{value}, "
            insert_query = insert_query[:-2] + ")"
            cur.execute(insert_query)
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False

    def edit_event(self, event_id : int, event_data : dict):
        conn, cur = self.get_handle()
        if conn and self.event_input_valid(event_data):
            if "event_id" in event_data:
                del event_data["event_id"]
            update_query = "UPDATE Events SET "
            for key in event_data.keys():
                if type(event_data[key]) == str:
                    update_query += f"{key} = '{event_data[key]}', "
                else:
                    update_query += f"{key} = {event_data[key]}, "
            update_query = update_query[:-2] + f" WHERE event_id = {event_id}"
            cur.execute(update_query)
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False
    
    def delete_event(self, event_id : int):
        conn, cur = self.get_handle()
        if conn:
            cur.execute(f"DELETE FROM Events WHERE event_id = {event_id}")
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False

    def season_input_valid(self, season_input : dict):
        allowed_fields = ["season_id", "season_title", "season_start_date", "season_end_date"]
        for key in season_input.keys():
            if key not in allowed_fields:
                return False
        return True

    def get_seasons(self):
        conn, cur = self.get_handle()
        rows = []
        if conn:
            cur.execute("SELECT * FROM Seasons")
            rows = [
                {
                    "season_id": entry[0],
                    "season_title": entry[1],
                    "season_start_date": entry[2],
                    "season_end_date": entry[3]
                } for entry in cur.fetchall()
            ]
            cur.close()
            conn.close()
        return rows

    def add_season(self, season_data : dict):
        conn, cur = self.get_handle()
        if conn and self.season_input_valid(season_data):
            insert_query = "INSERT INTO Seasons ("
            for key in season_data.keys():
                insert_query += f"{key}, "
            insert_query = insert_query[:-2] + ") VALUES ("
            for value in season_data.values():
                if type(value) == str:
                    insert_query += f"'{value}', "
                else:
                    insert_query += f"{value}, "
            insert_query = insert_query[:-2] + ")"
            cur.execute(insert_query)
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False

    def edit_season(self, season_id, season_data : dict):
        conn, cur = self.get_handle()
        if conn and self.season_input_valid(season_data):
            if "season_id" in season_data:
                del season_data["season_id"]
            update_query = "UPDATE Seasons SET "
            for key in season_data.keys():
                if type(season_data[key]) == str:
                    update_query += f"{key} = '{season_data[key]}', "
                else:
                    update_query += f"{key} = {season_data[key]}, "
            update_query = update_query[:-2] + f" WHERE season_id = {season_id}"
            cur.execute(update_query)
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False
    
    def delete_season(self, season_id):
        conn, cur = self.get_handle()
        if conn:
            cur.execute(f"DELETE FROM Seasons WHERE season_id = {season_id}")
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False

    def get_season_highscore(self, season_id : int):
        conn, cur = self.get_handle()
        rows = []
        if conn:
            cur.execute((f"SELECT team_id, team_name, SUM(points) AS highscore FROM ("
                         f"SELECT t.team_id AS team_id, t.team_name as team_name, m.team_a_points as points "
                         f"FROM Matches m, Teams t WHERE m.match_season = {season_id} AND t.team_id = m.team_a_id"
                         f" UNION ALL "
                         f"SELECT t.team_id AS team_id, t.team_name as team_name, m.team_b_points as points "
                         f"FROM Matches m, Teams t WHERE m.match_season = {season_id} AND t.team_id = m.team_b_id"
                         f") GROUP BY team_name ORDER BY highscore DESC"))
            rows = [{"team_id": entry[0], "team_name": entry[1], "team_score": entry[2]} for entry in cur.fetchall()]
            cur.close()
            conn.close()
        return rows

    def team_input_valid(self, team_input : dict):
        allowed_fields = ["team_id", "team_name"]
        for key in team_input.keys():
            if key not in allowed_fields:
                return False
        return True

    def get_teams(self):
        conn, cur = self.get_handle()
        if conn:
            cur.execute("SELECT team_id, team_name FROM Teams")
            rows = [
                {
                    "team_id": entry[0],
                    "team_name": entry[1]
                } for entry in cur.fetchall()
            ]
            cur.close()
            conn.close()
        return rows
    
    def add_team(self, team_data : dict):
        conn, cur = self.get_handle()
        if conn and self.team_input_valid(team_data):
            insert_query = "INSERT INTO Teams ("
            for key in team_data.keys():
                insert_query += f"{key}, "
            insert_query = insert_query[:-2] + ") VALUES ("
            for value in team_data.values():
                if type(value) == str:
                    insert_query += f"'{value}', "
                else:
                    insert_query += f"{value}, "
            insert_query = insert_query[:-2] + ")"
            cur.execute(insert_query)
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False
    
    def edit_team(self, team_id : int, team_data : dict):
        conn, cur = self.get_handle()
        if conn and self.team_input_valid(team_data):
            if "team_id" in team_data:
                del team_data["team_id"]
            update_query = "UPDATE Teams SET "
            for key in team_data.keys():
                if type(team_data[key]) == str:
                    update_query += f"{key} = '{team_data[key]}', "
                else:
                    update_query += f"{key} = {team_data[key]}, "
            update_query = update_query[:-2] + f" WHERE team_id = {team_id}"
            cur.execute(update_query)
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False
    
    def delete_team(self, team_id : int):
        conn, cur = self.get_handle()
        if conn:
            cur.execute(f"DELETE FROM Teams WHERE team_id = {team_id}")
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False

    def match_input_valid(self, match_input : dict):
        allowed_fields = ["match_id", "match_date", "match_start_time", "match_end_time",
                          "match_season", "team_a_id", "team_b_id", "team_a_points", "team_b_points"]
        for key in match_input.keys():
            if key not in allowed_fields:
                return False
        return True

    def get_matches(self):
        conn, cur = self.get_handle()
        if conn:
            cur.execute("SELECT * FROM Matches")
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
            cur.close()
            conn.close()
        return rows

    def get_match(self, match_id : int):
        conn, cur = self.get_handle()
        result = {}
        if conn:
            cur.execute(f"SELECT " 
                        f"m.match_id, m.match_date, m.match_start_time, m.match_end_time, t1.team_name,"
                        f"t2.team_name, m.team_a_points, m.team_b_points "
                        f"FROM Matches m, Teams t1, Teams t2 "
                        f"WHERE m.match_id = {match_id} AND m.team_a_id = t1.team_id AND m.team_b_id = t2.team_id")
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
            cur.close()
            conn.close()
        return result

    def get_season_matches(self, season_id : int):
        conn, cur = self.get_handle()
        rows = []
        if conn:
            cur.execute(f"SELECT " 
                        f"m.match_id, m.match_date, m.match_start_time, m.match_end_time, t1.team_name,"
                        f"t2.team_name, m.team_a_points, m.team_b_points "
                        f"FROM Matches m, Teams t1, Teams t2 "
                        f"WHERE m.match_season = {season_id} AND m.team_a_id = t1.team_id "
                        f"AND m.team_b_id = t2.team_id")
            rows = [{
                "match_id": entry[0],
                "match_date": entry[1],
                "match_start_time": entry[2],
                "match_end_time": entry[3],
                "team_a_name": entry[4],
                "team_b_name": entry[5],
                "team_a_points": entry[6],
                "team_b_points": entry[7]} for entry in cur.fetchall()]
            cur.close()
            conn.close()
        return rows

    def add_match(self, season_id : int, match_data : dict):
        conn, cur = self.get_handle()
        if conn and self.match_input_valid(match_data):
            insert_query = "INSERT INTO Matches (match_season, "
            for key in match_data.keys():
                insert_query += f"{key}, "
            insert_query = insert_query[:-2] + f") VALUES ({season_id}, "
            for value in match_data.values():
                if type(value) == str:
                    insert_query += f"'{value}', "
                else:
                    insert_query += f"{value}, "
            insert_query = insert_query[:-2] + ")"
            cur.execute(insert_query)
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False
    
    def edit_match(self, match_id : int, new_data : dict):
        conn, cur = self.get_handle()
        if conn and self.match_input_valid(new_data):
            if "match_id" in new_data:
                del new_data["match_id"]
            update_query = "UPDATE Matches SET "
            for key in new_data:
                if type(new_data[key]) == str:
                    update_query += f"{key} = '{new_data[key]}', "
                else:
                    update_query += f"{key} = {new_data[key]}, "
            update_query = update_query[:-2] + f" WHERE match_id = {match_id}"
                
            cur.execute(update_query)
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False
    
    def delete_match(self, match_id : int):
        conn, cur = self.get_handle()
        if conn:
            cur.execute(f"DELETE FROM Matches WHERE match_id = {match_id}")
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False
