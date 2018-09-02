from collections import defaultdict
from datetime import datetime
from dateutil import tz
import json
import os
from pathlib import Path
from time import sleep
os.chdir("/home/jovyan/work")

import arrow
import pandas as pd

from utils import print_information, send_request



def _get_play_type(play):
    return (set(play.keys()) - set(["description", "playStatus"])).pop()


def _unmarshall_jumpball(jumpball, game_id):
    result = {}
    
    # attributes
    result["gameID"] = game_id
    result["name"] = jumpball["description"]
    result["wonBy"] = jumpball["jumpBall"]["wonBy"]
    
    # relationships
    result["homePlayerID"] = jumpball["jumpBall"]["homePlayer"]["id"]
    result["awayPlayerID"] = jumpball["jumpBall"]["awayPlayer"]["id"]
    result["secondsElapsed"] = jumpball["playStatus"]["secondsElapsed"]
    result["quarter"] = jumpball["playStatus"]["quarter"]
    
    PARSED_GAMES["jumpball"].append(result)
    
    
def _unmarshall_fieldGoalAttempt(fieldGoalAttempt, game_id):
    result = {}
    
    # attributes
    result["gameID"] = game_id
    result["name"] = fieldGoalAttempt["description"]
    result["points"] = fieldGoalAttempt["fieldGoalAttempt"]["points"]
    result["result"] = fieldGoalAttempt["fieldGoalAttempt"]["result"]
    result["shotType"] = fieldGoalAttempt["fieldGoalAttempt"]["shotType"]
    
    # relationships
    result["shootingPlayerID"] = fieldGoalAttempt["fieldGoalAttempt"]["shootingPlayer"]["id"]
    result["secondsElapsed"] = fieldGoalAttempt["playStatus"]["secondsElapsed"]
    result["quarter"] = fieldGoalAttempt["playStatus"]["quarter"]
    
    # fragile values
    if fieldGoalAttempt["fieldGoalAttempt"]["blockingPlayer"] == None:
        result["blockingPlayerID"] = -1
    else:
        result["blockingPlayerID"] = fieldGoalAttempt["fieldGoalAttempt"]["blockingPlayer"]["id"]
    
    if fieldGoalAttempt["fieldGoalAttempt"]["assistingPlayer"] == None:
        result["assistingPlayerID"] = -1
    else:
        result["assistingPlayerID"] = fieldGoalAttempt["fieldGoalAttempt"]["assistingPlayer"]["id"]
    
    PARSED_GAMES["fieldGoalAttempt"].append(result)


def _unmarshall_turnover(turnover, game_id):
    result = {}
    
    # attributes
    result["gameID"] = game_id
    result["name"] = turnover["description"]
    result["isStolen"] = turnover["turnover"]["isStolen"]
    result["type"] = turnover["turnover"]["type"]
    
    # relationships
    result["lostByPlayerID"] = turnover["turnover"]["lostByPlayer"]["id"]
    result["secondsElapsed"] = turnover["playStatus"]["secondsElapsed"]
    result["quarter"] = turnover["playStatus"]["quarter"]
    
    # fragile values
    if turnover["turnover"]["stolenByPlayer"] == None:
        result["stolenByPlayerID"] = -1
    else:
        result["stolenByPlayerID"] = turnover["turnover"]["stolenByPlayer"]["id"]
    
    PARSED_GAMES["turnover"].append(result)


def _unmarshall_rebound(rebound, game_id):
    result = {}
    
    # attributes
    result["gameID"] = game_id
    result["name"] = rebound["description"]
    result["type"] = rebound["rebound"]["type"]
    
    # relationships
    result["secondsElapsed"] = rebound["playStatus"]["secondsElapsed"]
    result["quarter"] = rebound["playStatus"]["quarter"]
    
    # fragile values
    if rebound["rebound"]["retrievingPlayer"] == None:
        result["retrievingPlayerID"] = -1
    else:
        result["retrievingPlayerID"] = rebound["rebound"]["retrievingPlayer"]["id"]
    
    PARSED_GAMES["rebound"].append(result)


def _unmarshall_substitution(substitution, game_id):
    result = {}
    
    # attributes
    result["gameID"] = game_id
    result["name"] = substitution["description"]
    
    # relationships
    result["secondsElapsed"] = substitution["playStatus"]["secondsElapsed"]
    result["quarter"] = substitution["playStatus"]["quarter"]
    
    # fragile values
    if substitution["substitution"]["incomingPlayer"] == None:
        result["incomingPlayerID"] = -1
    else:
        result["incomingPlayerID"] = substitution["substitution"]["incomingPlayer"]["id"]
    
    if substitution["substitution"]["outgoingPlayer"] == None:
        result["outgoingPlayerID"] = -1
    else:
        result["outgoingPlayer"] = substitution["substitution"]["outgoingPlayer"]["id"]
    
    PARSED_GAMES["substitution"].append(result)


def _unmarshall_freeThrowAttempt(freeThrowAttempt, game_id):
    result = {}
    
    # attributes
    result["gameID"] = game_id
    result["name"] = freeThrowAttempt["description"]
    result["attemptNum"] = freeThrowAttempt["freeThrowAttempt"]["attemptNum"]
    result["result"] = freeThrowAttempt["freeThrowAttempt"]["result"]
    result["totalAttempts"] = freeThrowAttempt["freeThrowAttempt"]["totalAttempts"]
    
    # relationships
    result["shootingPlayerID"] = freeThrowAttempt["freeThrowAttempt"]["shootingPlayer"]["id"]
    result["secondsElapsed"] = freeThrowAttempt["playStatus"]["secondsElapsed"]
    result["quarter"] = freeThrowAttempt["playStatus"]["quarter"]
    
    PARSED_GAMES["freeThrowAttempt"].append(result)


def _unmarshall_violation(violation, game_id):
    result = {}
    
    # attributes
    result["gameID"] = game_id
    result["name"] = violation["description"]
    result["teamOrPersonal"] = violation["violation"]["teamOrPersonal"]
    
    # relationships
    result["teamAbbreviation"] = violation["violation"]["team"]["abbreviation"]
    result["teamAbbreviation"] = violation["violation"]["team"]["abbreviation"]
    result["secondsElapsed"] = violation["playStatus"]["secondsElapsed"]
    result["quarter"] = violation["playStatus"]["quarter"]
    
    # fragile values
    if violation["violation"]["player"] == None:
        result["playerID"] = -1
    else:
        result["playerID"] = violation["violation"]["player"]["id"]
    
    PARSED_GAMES["violation"].append(result)


def _unmarshall_foul(foul, game_id):
    result = {}
    
    # attributes
    result["gameID"] = game_id
    result["name"] = foul["description"]
    result["teamAbbreviation"] = foul["foul"]["team"]["abbreviation"]
    
    # relationships
    result["secondsElapsed"] = foul["playStatus"]["secondsElapsed"]
    result["quarter"] = foul["playStatus"]["quarter"]
    
    # fragile values
    if foul["foul"]["penalizedPlayer"] == None:
        result["penalizedPlayerID"] = -1
    else:
        result["penalizedPlayerID"] = foul["foul"]["penalizedPlayer"]["id"]

    if foul["foul"]["drawnByPlayer"] == None:
        result["drawnByPlayerID"] = -1
    else:
        result["drawnByPlayerID"] = foul["foul"]["drawnByPlayer"]["id"]

    if  foul["foul"]["isPersonal"]:
        result["type"] = "personal"
    elif  foul["foul"]["isTechnical"]:
        result["type"] = "technical"
    elif  foul["foul"]["isFlagrant1"]:
        result["type"] = "flagrant1"
    elif  foul["foul"]["isFlagrant2"]:
        result["type"] = "flagrant2"
    else:
        result["type"] = "unnkown"

    PARSED_GAMES["foul"].append(result)


def _get_datetime(team_abbreviaion, dt):
    if team_abbreviaion in [
        "NYK", "BRO", "BOS", "PHI", 
        "WAS", "CHA", "ATL", "ORL", 
        "MIA", "TOR", "CLE", "DET", "IND"]:
        time_zone = tz.gettz("US/Eastern")
    elif team_abbreviaion in [
        "CHI", "MIN", "DAL", "SAS", 
        "OKL", "MEM", "HOU", "MIL", "NOP"]:
        time_zone = tz.gettz("US/Central")
    elif team_abbreviaion in ["DEN", "PHX", "UTA"]:
        time_zone = tz.gettz("US/Mountain")
    elif team_abbreviaion in [
        "POR", "GSW", "LAL", "LAC", "SAC"]:
        time_zone = tz.gettz("US/Pacific")
    else:
        print("Error with timezones")
    return datetime.fromtimestamp(arrow.get(dt).timestamp, time_zone)


def _unmarshall_season_game(game):
    date = _get_datetime(game["schedule"]["homeTeam"]["abbreviation"], game["schedule"]["startTime"]).strftime("%Y%m%d")
    away = game["schedule"]["awayTeam"]["abbreviation"]
    home = game["schedule"]["homeTeam"]["abbreviation"]
    return "-".join([date, away, home])

@print_information
def generate_game_names():
    games = []
    for season in SEASONS:
        print("Processing: {season}".format(**locals()))
        req = send_request("https://api.mysportsfeeds.com/v2.0/pull/nba/{season}/games.json".format(**locals()))
        fetched_season = json.loads(req.text)
        for game in fetched_season.get("games"):
            games.append({"season": season, "game": _unmarshall_season_game(game), "id": game["schedule"]["id"]})
    return games


@print_information
def fetch_games(games):
    failed_urls = []
    for idx, g in enumerate(games, 1):
        s = "https://api.mysportsfeeds.com/v2.0/pull/nba/{season}/games/{game}/playbyplay.json".format(**g)

        req = send_request(s)

        if req.status_code == 200:
            pbp = json.loads(req.text)
            print("[{idx:04d}/{total}]: fetched {game}({id})".format(idx=idx, total=len(games), **g))
            for play in pbp.get("plays"):
                play_type = _get_play_type(play)
                UNMARSHALL[play_type](play, g["id"])
        elif req.status_code == 429:
            print("Fetched too much, sleeping for 5 minutes")
            sleep(5*60 + 30)
            req = send_request(s)
            pbp = json.loads(req.text)
            print("[{idx:04d}/{total}]: fetched {game}({id})".format(idx=idx, total=len(games), **g))
            for play in pbp.get("plays"):
                play_type = _get_play_type(play)
                UNMARSHALL[play_type](play, g["id"])
        else:
            print("No data for {game}({id})".format(**g))
            failed_urls.append(s)
    for k in PARSED_GAMES:
        df = pd.DataFrame.from_records(PARSED_GAMES.get(k))
        df.to_csv("./data/generated/play_by_play/play_by_play_{k}.csv".format(**locals()), index=False)   


UNMARSHALL = {
    "jumpBall": _unmarshall_jumpball,
    "fieldGoalAttempt": _unmarshall_fieldGoalAttempt,
    "turnover": _unmarshall_turnover,
    "foul": _unmarshall_foul,
    "rebound": _unmarshall_rebound,
    "substitution": _unmarshall_substitution,
    "freeThrowAttempt": _unmarshall_freeThrowAttempt,
    "violation": _unmarshall_violation
}

PARSED_GAMES = defaultdict(list)

SEASONS = [
    "2015-2016-regular",
    "2016-playoff",
    "2016-2017-regular",
    "2017-playoff",
    "2017-2018-regular"
]

if __name__ == "__main__":
    if input("Fetch MySportFeeds PlayByPlay API? (NO/yes)") == "yes":
        p = Path("./data/generated/play_by_play")
        if not p.exists():
            p.mkdir(parents=True)
        games = generate_game_names()
        fetch_games(games)
        print(">> Files can be found under ./data/generated <<")