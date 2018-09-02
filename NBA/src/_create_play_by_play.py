import os
os.chdir("/home/jovyan/work")

import pandas as pd
from tqdm import tqdm

from models import (
    Foul,
    FieldGoalAttempt,
    FreeThrowAttempt, 
    Game, 
    JumpBall, 
    Player, 
    Rebound, 
    Substitution, 
    Turnover, 
    Violation,
)
from utils import init_connection, print_information



@print_information
def create_jumpballs():
    df = pd.read_csv("./data/play_by_play_files/play_by_play_jumpball.csv")
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        jb = JumpBall()
        jb.name = row["name"]
        jb.won_by = row["wonBy"]
        jb.elapsed_seconds = row["secondsElapsed"]
        jb.quarter = row["quarter"]
        jb.save()

        jb.away_player.connect(Player.nodes.get(msfID=row["awayPlayerID"]))
        jb.home_player.connect(Player.nodes.get(msfID=row["homePlayerID"]))
        jb.game.connect(Game.nodes.get(game_id=row["gameID"]))


@print_information
def create_violation():
    df = pd.read_csv("./data/play_by_play_files/play_by_play_violation.csv")
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        v = Violation()
        v.name = row["name"]
        v.team_abbreviation = row["teamAbbreviation"]
        v.vioalation_type = row["teamOrPersonal"]
        v.elapsed_seconds = row["secondsElapsed"]
        v.quarter = row["quarter"]
        v.save()

        v.game.connect(Game.nodes.get(game_id=row["gameID"]))
        if v.vioalation_type == "PERSONAL":
            v.player.connect(Player.nodes.get(msfID=row["playerID"]))


@print_information
def create_turnover():
    df = pd.read_csv("./data/play_by_play_files/play_by_play_turnover.csv")
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        t = Turnover()
        t.name = row["name"]
        t.is_stolen = row["isStolen"]
        t.turnover_type = row["type"]
        t.elapsed_seconds = row["secondsElapsed"]
        t.quarter = row["quarter"]
        t.save()

        t.lost_by_player.connect(Player.nodes.get(msfID=row["lostByPlayerID"]))
        t.game.connect(Game.nodes.get(game_id=row["gameID"]))
        if t.is_stolen:
            t.stolen_by_player.connect(Player.nodes.get(msfID=row["stolenByPlayerID"]))


@print_information
def create_fouls():
    df = pd.read_csv("./data/play_by_play_files/play_by_play_foul.csv")
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        f = Foul()
        f.name = row["name"]
        f.team_abbreviation = row["teamAbbreviation"]
        f.foul_type = row["type"]
        f.elapsed_seconds = row["secondsElapsed"]
        f.quarter = row["quarter"]
        f.save()

        if row["penalizedPlayerID"] != -1:
            f.penalized_player.connect(Player.nodes.get(msfID=row["penalizedPlayerID"]))
        if row["drawnByPlayerID"] != -1:
            f.drawn_by_player.connect(Player.nodes.get(msfID=row["drawnByPlayerID"]))
        f.game.connect(Game.nodes.get(game_id=row["gameID"]))


@print_information
def create_field_goal_attempts():
    df = pd.read_csv("./data/play_by_play_files/play_by_play_fieldGoalAttempt.csv")
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        fga = FieldGoalAttempt()
        fga.name = row["name"]
        fga.points = row["points"]
        fga.result = row["result"]
        fga.shot_type = row["shotType"]
        fga.elapsed_seconds = row["secondsElapsed"]
        fga.quarter = row["quarter"]
        fga.save()

        fga.shooting_player.connect(Player.nodes.get(msfID=row["shootingPlayerID"]))
        if row["assistingPlayerID"] != -1:
            fga.assisting_player.connect(Player.nodes.get(msfID=row["assistingPlayerID"]))
        if row["blockingPlayerID"] != -1:
            fga.blocking_player.connect(Player.nodes.get(msfID=row["blockingPlayerID"]))


@print_information
def create_rebound():
    df = pd.read_csv("./data/play_by_play_files/play_by_play_rebound.csv")
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        r = Rebound()
        r.name = row["name"]
        r.rebound_type = row["type"]
        r.elapsed_seconds = row["secondsElapsed"]
        r.quarter = row["quarter"]
        r.save()
        if row["retrievingPlayerID"] != -1:
            r.retrieving_player.connect(Player.nodes.get(msfID=row["retrievingPlayerID"]))
        r.game.connect(Game.nodes.get(game_id=row["gameID"]))


@print_information
def create_substitution():
    df = pd.read_csv("./data/play_by_play_files/play_by_play_substitution.csv")

    # little prep
    df.fillna(-1, inplace=True)
    df.drop("outgoingPlayerID", axis=1, inplace=True)
    df["outgoingPlayer"] = df["outgoingPlayer"].astype(int)
    df.columns = ['gameID', 'incomingPlayerID', 'name', 'outgoingPlayerID', 'quarter', 'secondsElapsed']

    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        s = Substitution()
        s.name =  row["name"]
        s.elapsed_seconds = row["secondsElapsed"]
        s.quarter = row["quarter"]
        s.save()

    if row["incomingPlayerID"] != -1:
        s.incoming_player.connect(Player.nodes.get(msfID=row["incomingPlayerID"]))
    if row["outgoingPlayerID"] != -1:
        s.outgoing_player.connect(Player.nodes.get(msfID=row["outgoingPlayerID"]))


@print_information
def create_free_throw_attempt():
    df = pd.read_csv("./data/play_by_play_files/play_by_play_freeThrowAttempt.csv")
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        fta = FreeThrowAttempt()
        fta.name = row["name"]
        fta.number = row["attemptNum"]
        fta.total_attempts = row["totalAttempts"]
        fta.result = row["result"]
        fta.elapsed_seconds = row["secondsElapsed"]
        fta.quarter = row["quarter"]
        fta.save()

        if row["shootingPlayerID"] != -1:
            fta.shooting_player.connect(Player.nodes.get(msfID=row["shootingPlayerID"]))
        fta.game.connect(Game.nodes.get(game_id=row["gameID"]))


if __name__ == "__main__":
    init_connection()
    create_jumpballs()
    create_violation()
    create_turnover()
    create_fouls()
    create_field_goal_attempts()
    create_rebound()
    create_substitution()
    create_free_throw_attempt()