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
    
    def create_tables(self):
        conn, cur = self.get_handle()
        if conn:
            cur.execute("CREATE TABLE IF NOT EXISTS Seasons(season_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "season_title TEXT NOT NULL)")
            conn.commit()
            cur.execute("CREATE TABLE IF NOT EXISTS Matches(match_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "match_title TEXT NOT NULL, season_id INTEGER REFERENCES Seasons(season_id))")
            conn.commit()
            cur.execute("CREATE TABLE IF NOT EXISTS Teams(team_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                        " team_name TEXT NOT NULL)")
            conn.commit()
            cur.execute("CREATE TABLE IF NOT EXISTS Scores(score_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                        " season_id INTEGER REFERENCES Seasons(season_id), team_id INTEGER REFERENCES"
                        " Teams(team_id) NOT NULL, team_score INTEGER NOT NULL)")
            conn.commit()
            cur.close()
            conn.close()
    
    def add_mock_data(self, override : bool = True):
        conn, cur = self.get_handle()
        if conn:
            try:
                if override:
                    cur.execute("DELETE FROM Seasons WHERE season_id BETWEEN 0 AND 2")
                    conn.commit()
                    cur.execute("DELETE FROM Matches WHERE match_id BETWEEN 0 AND 5")
                    conn.commit()
                    cur.execute("DELETE FROM Teams WHERE team_id BETWEEN 0 AND 3")
                    conn.commit()
                    cur.execute("DELETE FROM Scores WHERE score_id BETWEEN 0 AND 8")
                    conn.commit()
                cur.execute("INSERT INTO Seasons(season_id, season_title) VALUES "
                            "(0, 'Season 1'),"
                            "(1, 'Season 2'),"
                            "(2, 'Season 3')")
                conn.commit()
                cur.execute("INSERT INTO Matches(match_id, match_title, season_id) VALUES "
                            "(0, 'Match 1 (Season 1)', 0),"
                            "(1, 'Match 2 (Season 1)', 0),"
                            "(2, 'Match 1 (Season 2)', 1),"
                            "(3, 'Match 1 (Season 3)', 2),"
                            "(4, 'Match 2 (Season 3)', 2),"
                            "(5, 'Match 3 (Season 3)', 2)")
                conn.commit()
                cur.execute("INSERT INTO Teams(team_id, team_name) VALUES "
                            "(0, 'Team 1'),"
                            "(1, 'Team 2'),"
                            "(2, 'Team 3')")
                conn.commit()
                cur.execute("INSERT INTO Scores(score_id, season_id, team_id, team_score) VALUES "
                            "(0, 0, 0, 2000), (1, 0, 2, 1000), (2, 0, 1, 500),"
                            "(3, 1, 1, 100), (4, 1, 0, 50),"
                            "(5, 2, 2, 5000), (6, 2, 0, 1000), (7, 2, 3, 100), (8, 2, 1, 50)")
                conn.commit()
            except sqlite3.Error as error:
                print(f"Sqlite error while adding mock data: {error}")
            cur.close()
            conn.close()

    def get_seasons(self):
        conn, cur = self.get_handle()
        rows = []
        if conn:
            cur.execute("SELECT * FROM Seasons")
            rows = [{"season_id": entry[0], "season_title": entry[1]} for entry in cur.fetchall()]
            cur.close()
            conn.close()
        return rows

    def get_season_matches(self, season_id : int):
        conn, cur = self.get_handle()
        rows = []
        if conn:
            cur.execute(f"SELECT match_id, match_title FROM Matches WHERE season_id = {season_id}")
            rows = [{"match_id": entry[0], "match_title": entry[1]} for entry in cur.fetchall()]
            cur.close()
            conn.close()
        return rows

    def get_season_highscore(self, season_id : int):
        conn, cur = self.get_handle()
        rows = []
        if conn:
            cur.execute((f"SELECT team.team_id, team.team_name, score.team_score FROM Scores score,"
                         f" Teams team WHERE score.season_id = {season_id} AND score.team_id ="
                         f" team.team_id ORDER BY score.team_score DESC"))
            rows = [{"team_id": entry[0], "team_name": entry[1], "team_score": entry[2]} for entry in cur.fetchall()]
            cur.close()
            conn.close()
        return rows
    
    def get_match(self, match_id : int):
        conn, cur = self.get_handle()
        result = {}
        if conn:
            cur.execute((f"SELECT match.match_id, match.match_title, season.season_title FROM"
                         f" Matches match, Seasons season WHERE match_id = {match_id} AND"
                         f" match.season_id = season.season_id"))
            row = cur.fetchall()
            if len(row) > 0:
                result = {"match_id": row[0][0], "match_title": row[0][1], "season_title": row[0][2]}
            cur.close()
            conn.close()
        return result
    
    def edit_match(self, match_id : int, new_data : dict):
        conn, cur = self.get_handle()
        if conn:
            cur.execute(f"UPDATE Matches SET match_title = '{new_data['match_title']}' WHERE match_id = {match_id}")
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False
