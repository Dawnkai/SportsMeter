CREATE TABLE IF NOT EXISTS Seasons (
    season_id INTEGER PRIMARY KEY AUTOINCREMENT,
    season_title TEXT NOT NULL,
    season_start_date TEXT NOT NULL,
    season_end_date TEXT NULL
);

CREATE TABLE IF NOT EXISTS Teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_date TEXT NOT NULL,
    match_start_time TEXT NOT NULL,
    match_end_time TEXT NULL,
    match_season INTEGER REFERENCES Seasons(season_id),
    team_a_id INTEGER REFERENCES Teams(team_id),
    team_b_id INTEGER REFERENCES Teams(team_id),
    team_a_points INTEGER NULL,
    team_b_points INTEGER NULL
);

CREATE TABLE IF NOT EXISTS Notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    notification_title TEXT NOT NULL,
    notification_description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    player_gender TEXT NOT NULL,
    player_team INTEGER REFERENCES Teams(team_id) NULL
);
