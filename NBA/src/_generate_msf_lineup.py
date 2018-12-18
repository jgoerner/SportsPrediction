from dateutil import tz
from datetime import datetime
import json
import os
from pathlib import Path
os.chdir("/home/jovyan/work")
from time import sleep

import arrow
import pandas as pd
from utils import print_information, send_request


# iterate games
SEASONS = [
    "2015-2016-regular",
    "2016-playoff",
    "2016-2017-regular",
    "2017-playoff",
    "2017-2018-regular"
]

PARSED_GAMES = []


def generate_game_names():
    games = []
    for season in SEASONS:
        print("Processing: {season}".format(**locals()))
        fetched_season = send_request("https://api.mysportsfeeds.com/v2.0/pull/nba/{season}/games.json".format(**locals()))
        for game in fetched_season.get("games"):
            games.append({"season": season, "game": _unmarshall_season_game(game), "id": game["schedule"]["id"]})
    return games


def _unmarshall_season_game(game):
    date = _get_datetime(game["schedule"]["homeTeam"]["abbreviation"], game["schedule"]["startTime"]).strftime("%Y%m%d")
    away = game["schedule"]["awayTeam"]["abbreviation"]
    home = game["schedule"]["homeTeam"]["abbreviation"]
    return "-".join([date, away, home])


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


def _unmarshall_lineup(lineup, game_id):
    game_lineup = {"game_id": game_id }
    team_ids = [
        team["team"]["abbreviation"]
        for team in lineup
    ]
    game_lineup.update({
        "t_{}".format(idx):t
        for (idx,t)
        in enumerate(team_ids, 1)
    })
    lu_type = "actual" if lineup[0]["actual"] else "expected"
    player_ids = [
        position["player"]["id"]
        for team in lineup
        for position in team[lu_type]["lineupPositions"]
        if position["position"].startswith("Starter") 
    ]
    game_lineup.update({
        "p_{:02d}".format(idx):p
        for (idx,p)
        in enumerate(player_ids, 1)
    })
    return game_lineup


@print_information
def fetch_games(games):
    failed_urls = []
    for idx, g in enumerate(games, 1):
        s = "https://api.mysportsfeeds.com/v2.0/pull/nba/{season}/games/{game}/lineup.json".format(**g)

        req = send_request(s, raw=True)

        if req.status_code == 200:
            lu = json.loads(req.text).get("teamLineups")
            print("[{idx:04d}/{total}]: fetched {game}({id})".format(idx=idx, total=len(games), **g))
            PARSED_GAMES.append(_unmarshall_lineup(lu, g["id"]))
        elif req.status_code == 429:
            print("Fetched too much, sleeping for 5 minutes")
            sleep(5*60 + 30)
            req = send_request(s, raw=True)
            lu = json.loads(req.text).get("teamLineups")
            print("[{idx:04d}/{total}]: fetched {game}({id})".format(idx=idx, total=len(games), **g))
            PARSED_GAMES.append(_unmarshall_lineup(lu, g["id"]))
        else:
            print("No data for {game}({id})".format(**g))
            failed_urls.append(s)

    df = pd.DataFrame.from_records(PARSED_GAMES)
    df.to_csv("./data/generated/lineups.csv", index=False)   


if __name__ == "__main__":
    if input("Fetch MySportFeeds Player API? (NO/yes)") == "yes":
        p = Path("./data/generated")
        if not p.exists():
            p.mkdir(parents=True)
        games = generate_game_names()
        fetch_games(games)        
        print(">> Files can be found under ./data/generated <<")