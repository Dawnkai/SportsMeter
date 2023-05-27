import json
import pytest

from os import path, remove
from .sqlite_driver import SqliteDriver
from backend.exceptions import InvalidInputError

class TestSqlite:
    @pytest.fixture
    def database(self):
        db = SqliteDriver("test.db")
        db.create_tables("create.sql")
        yield db
        if path.exists("test.db"):
            remove("test.db")

    def test_get_events(self, database):
        database.insert_from_csv("Events", "test_input/events.csv", ";")
        events = database.get_events()
        with open("test_output/events.json", encoding="utf-8") as events_results:
            expected_result = json.load(events_results)
            assert events == expected_result

    def test_add_event(self, database):
        database.add_event(
            {
                "event_title": "test_event",
                "event_description": ""
            }
        )
        events = database.get_events()
        assert events == [
            {
                "event_id": 1,
                "event_title": "test_event",
                "event_description": ""
            }
        ]

    def test_edit_event(self, database):
        database.insert_from_csv("Events", "test_input/events.csv", ";")
        database.edit_event(0, {"event_title" : "edited title"})
        events = database.get_events()
        assert events[0]["event_title"] == "edited title"
    
    def test_delete_event(self, database):
        database.insert_from_csv("Events", "test_input/events.csv", ";")
        database.delete_event(0)
        events = database.get_events()
        assert len(events) == 3 and events[0]["event_id"] != 0

    def test_wrong_event_fields(self, database):
        with pytest.raises(InvalidInputError):
            database.add_event(
                {
                    "event_title": "wrong_event",
                    "event_description": "",
                    "illegal_field": "value"
                }
            )

    def test_get_seasons(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        seasons = database.get_seasons()
        with open("test_output/seasons.json", encoding="utf-8") as seasons_results:
            expected_result = json.load(seasons_results)
            assert seasons == expected_result
    
    def test_add_season(self, database):
        database.add_season(
            {
                "season_title": "test",
                "season_start_date": "19990101",
                "season_end_date": "19990110"
            }
        )
        seasons = database.get_seasons()
        assert seasons[0] == {
            "season_id": 1,
            "season_title": "test",
            "season_start_date": "19990101",
            "season_end_date": "19990110"
        }
    
    def test_edit_season(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.edit_season(1, {"season_title" : "edited season"})
        seasons = database.get_seasons()
        assert seasons[1]["season_title"] == "edited season"
    
    def test_delete_season(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.delete_season(1)
        seasons = database.get_seasons()
        assert len(seasons) == 1 and seasons[0]["season_id"] == 0

    def test_wrong_season_fields(self, database):
        with pytest.raises(InvalidInputError):
            database.add_season(
                {
                    "season_title": "test",
                    "season_start_date": "19990101",
                    "season_end_date": "19990110",
                    "illegal_field": "some value"
                }
            )

    def test_get_season_highscore(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        highscore = database.get_season_highscore(1)
        assert highscore == [
            {
                "team_id": 2,
                "team_name": "Warszawa Unicorns",
                "team_score": 125
            },
            {
                "team_id": 8,
                "team_name": "Lublin Lynx",
                "team_score": 40
            },
            {
                "team_id": 1,
                "team_name": "Łódź Pirates",
                "team_score": 35
            }
        ]

    def test_get_teams(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        teams = database.get_teams()
        with open("test_output/teams.json", encoding="utf-8") as teams_results:
            expected_result = json.load(teams_results)
            assert teams == expected_result
    
    def test_add_team(self, database):
        database.add_team({"team_name": "test team"})
        teams = database.get_teams()
        assert teams == [{"team_id": 1, "team_name": "test team"}]
    
    def test_edit_team(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.edit_team(0, {"team_name": "edited name"})
        teams = database.get_teams()
        assert teams[0]["team_name"] == "edited name"
    
    def test_delete_team(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.delete_team(0)
        teams = database.get_teams()
        assert len(teams) == 8 and teams[0]["team_id"] != 0

    def test_wrong_team_data(self, database):
        with pytest.raises(InvalidInputError):
            database.add_team({"team_name": "test team", "illegal_field": ""})

    def test_get_matches(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        matches = database.get_matches()
        with open("test_output/matches.json", encoding="utf-8") as matches_results:
            expected_result = json.load(matches_results)
            assert matches == expected_result

    def test_get_match(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        match = database.get_match(0)
        assert match == {
            "match_id": 0,
            "match_date": "20220312",
            "match_start_time": "113000",
            "match_end_time": "123000",
            "team_a_name": "Poznań Capricorns",
            "team_b_name": "Łódź Pirates",
            "team_a_points": 50,
            "team_b_points": 100
        }

    def test_get_season_matches(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        matches = database.get_season_matches(1)
        assert matches == [
            {
                "match_id": 4,
                "match_date": "20220720",
                "match_start_time": "143000",
                "match_end_time": "153000",
                "team_a_name": "Łódź Pirates",
                "team_b_name": "Warszawa Unicorns",
                "team_a_points": 35,
                "team_b_points": 65
            },
            {
                "match_id": 5,
                "match_date": "20220810",
                "match_start_time": "090500",
                "match_end_time": "112000",
                "team_a_name": "Warszawa Unicorns",
                "team_b_name": "Lublin Lynx",
                "team_a_points": 60,
                "team_b_points": 40
            }
        ]

    def test_add_match(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.add_match(1, {
            "match_date": "20220720",
            "match_start_time": "143000",
            "match_end_time": "153000",
            "team_a_id": 0,
            "team_b_id": 1,
            "team_a_points": 35,
            "team_b_points": 65
        })
        matches = database.get_season_matches(1)
        assert matches == [
            {
                "match_id": 1,
                "match_date": "20220720",
                "match_start_time": "143000",
                "match_end_time": "153000",
                "team_a_name": "Poznań Capricorns",
                "team_b_name": "Łódź Pirates",
                "team_a_points": 35,
                "team_b_points": 65
            }
        ]
    
    def test_wrong_match_fields(self, database):
        with pytest.raises(InvalidInputError):
            database.add_match(1, {
                "match_date": "20220720",
                "match_start_time": "143000",
                "match_end_time": "153000",
                "team_a_id": 0,
                "team_b_id": 1,
                "team_a_points": 35,
                "team_b_points": 65,
                "illegal_field": ""
            })

    def test_edit_match(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.edit_match(0, {"team_a_points" : 200})
        match = database.get_match(0)
        assert match["team_a_points"] == 200
    
    def test_get_empty_match(self, database):
        match = database.get_match(0)
        assert match == {}

    def test_delete_match(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.delete_match(0)
        matches = database.get_matches()
        assert matches[0]["match_id"] != 0
