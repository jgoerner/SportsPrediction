import dateutil.parser
import os
from pathlib import Path
os.chdir("/home/jovyan/work")

import pandas as pd
from utils import print_information, send_request



COLUMNS=[
    "Date", 
    "Start (ET)", 
    "Visitor/Neutral", 
    "PTS",
    "Home/Neutral", 
    "PTS.1", 
    "OT", 
    "Attend.", 
    "game_type", 
    "game_name",
    "game_id"
]


def unmarshall_game(game, game_type="regular_season"):
    """Unmarshal a JSON to a proper row
    
    Paramters
    ---------
    game: dict,
        game JSON fetched from msf
    game_type: string, default="regular_season",
        game type ("regular_season"/"playoff")
    """
    row = {}
    row["game_id"] = game["schedule"]["id"]
    date = dateutil.parser.parse(game["schedule"]["startTime"])
    # Date
    row["Date"] = date.strftime("%Y-%m-%d")
    # Start (ET)
    # ! NO TIME
    row["Start (ET)"] = date.strftime("%I:%M %p")
    # Visitor/Neutral
    row["Visitor/Neutral"] = game["schedule"]["awayTeam"]["abbreviation"]
    # PTS
    row["PTS"] = game["score"]["awayScoreTotal"]
    # Home/Neutral
    row["Home/Neutral"] = game["schedule"]["homeTeam"]["abbreviation"]
    # PTS.1
    row["PTS.1"] = game["score"]["homeScoreTotal"]
    # OT
    row["OT"] = 1 if len(game["score"]["quarters"]) > 4 else 0
    # Attend.
    # ! NO INFO
    row["Attend."] = None
    # game_type
    row["game_type"] = game_type
    # game_name
    row["game_name"] = row["Visitor/Neutral"] + " at " + row["Home/Neutral"]
    return row


@print_information
def create_season_1516():
    result1516_reg = \
        send_request("https://api.mysportsfeeds.com/v2.0/pull/nba/2015-2016-regular/games.json")
    games_reg1516 = \
        list(map(lambda game: unmarshall_game(game), result1516_reg.get("games")))
    result1516_po = \
        send_request("https://api.mysportsfeeds.com/v2.0/pull/nba/2016-playoff/games.json")
    games_po1516 = \
        list(map(lambda game: unmarshall_game(game), result1516_po.get("games")))
    df_reg = pd.DataFrame.from_records(games_reg1516)
    df_po = pd.DataFrame.from_records(games_po1516)
    df = df_reg.append(df_po)
    df = df[COLUMNS]
    df.reset_index(drop=True, inplace=True)
    df.to_csv("./data/generated/season_files/season1516.csv", index=False)


@print_information
def create_season_1617():
    result1617_reg = \
        send_request("https://api.mysportsfeeds.com/v2.0/pull/nba/2016-2017-regular/games.json")
    games_reg1617 = \
        list(map(lambda game: unmarshall_game(game), result1617_reg.get("games")))
    result1617_po = \
        send_request("https://api.mysportsfeeds.com/v2.0/pull/nba/2017-playoff/games.json")
    games_po1617 = \
        list(map(lambda game: unmarshall_game(game), result1617_po.get("games")))
    df_reg = pd.DataFrame.from_records(games_reg1617)
    df_po = pd.DataFrame.from_records(games_po1617)
    df = df_reg.append(df_po)
    df = df[COLUMNS]
    df.reset_index(drop=True, inplace=True)
    df.to_csv("./data/generated/season_files/season1617.csv", index=False)


@print_information
def create_season_1718():
    result1718_reg = \
        send_request("https://api.mysportsfeeds.com/v2.0/pull/nba/2017-2018-regular/games.json")
    games_reg1718 = \
        list(map(lambda game: unmarshall_game(game), result1718_reg.get("games")))
    result1718_po = \
        send_request("https://api.mysportsfeeds.com/v2.0/pull/nba/2018-playoff/games.json")
    games_po1718 = \
        list(map(lambda game: unmarshall_game(game), result1718_po.get("games")))
    df_reg = pd.DataFrame.from_records(games_reg1718)
    df_po = pd.DataFrame.from_records(games_po1718)
    df = df_reg.append(df_po)
    df = df[COLUMNS]
    df.reset_index(drop=True, inplace=True)
    df.to_csv("./data/generated/season_files/season1718.csv", index=False)

    
if __name__ == "__main__":
    if input("Fetch MySportFeeds Season API? (NO/yes)") == "yes":
        p = Path("./data/generated/season_files")
        if not p.exists():
            p.mkdir(parents=True)
        create_season_1516()
        create_season_1617()
        create_season_1718()
        print(">> Files can be found under ./data/generated <<")