# Necessary to import custom modules
from datetime import datetime
import os
os.chdir("/home/jovyan/work")

import pandas as pd

from utils import init_connection, print_information
from models import Arena, Date, Game, Score, Season, Team


@print_information
def connect_match_data_season_1516():
    df = pd.read_csv("./data/season_files/season1516.csv")
    n_rels = 0
    n_nodes = 0
    for _, row in df.iterrows():
        # NODES
        # Hometeam
        ht = Team.nodes.get(abbreviation=row["Home/Neutral"])
        # Visitor
        vt = Team.nodes.get(abbreviation=row["Visitor/Neutral"])
        # HomeScore
        hs = Score(score=row["PTS.1"]).save()
        # VisitorScore
        vs = Score(score=row["PTS"]).save()
        # Arena
        a = ht.arena.get()
        # Season
        s = Season.get_or_create(
            {"name": "2015/2016"}
        )[0]
        # Date
        d = Date.get_or_create(
            {"datetime": datetime.strptime(row["Date"] + " " + row["Start (ET)"], "%Y-%m-%d %I:%M %p")}
        )[0]
        # Game
        g = Game(
            game_id=row["game_id"],
            game_name=row["game_name"],
            game_type=row["game_type"],
            ot=row["OT"]).save() 
        n_nodes += 1
        
        # RELATIONSHIPS
        # Team -> Score
        ht.scored.connect(hs)
        vt.scored.connect(vs)
        # Score -> Game
        hs.in_game.connect(g)
        vs.in_game.connect(g)
        # Game -> Season
        g.season.connect(s)
        # Game -> Date
        g.date.connect(d)
        # Game -> Arena
        g.arena.connect(a)
        n_rels += 7
    print("created (approx:) {} nodes and {} relationships".format(n_nodes, n_rels))

@print_information
def connect_match_data_season_1617():
    df = pd.read_csv("./data/season_files/season1617.csv")
    n_rels = 0
    n_nodes = 0
    for _, row in df.iterrows():
        # NODES
        # Hometeam
        ht = Team.nodes.get(abbreviation=row["Home/Neutral"])
        # Visitor
        vt = Team.nodes.get(abbreviation=row["Visitor/Neutral"])
        # HomeScore
        hs = Score(score=row["PTS.1"]).save()
        # VisitorScore
        vs = Score(score=row["PTS"]).save()
        # Arena
        a = ht.arena.get()
        # Season
        s = Season.get_or_create(
            {"name": "2016/2017"}
        )[0]
        # Date
        d = Date.get_or_create(
            {"datetime": datetime.strptime(row["Date"] + " " + row["Start (ET)"], "%Y-%m-%d %I:%M %p")}
        )[0]
        # Game
        g = Game(
            game_id=row["game_id"],
            game_name=row["game_name"],
            game_type=row["game_type"],
            ot=row["OT"]).save() 
        n_nodes += 1
        
        # RELATIONSHIPS
        # Team -> Score
        ht.scored.connect(hs)
        vt.scored.connect(vs)
        # Score -> Game
        hs.in_game.connect(g)
        vs.in_game.connect(g)
        # Game -> Season
        g.season.connect(s)
        # Game -> Date
        g.date.connect(d)
        # Game -> Arena
        g.arena.connect(a)
        n_rels += 7
    print("created (approx:) {} nodes and {} relationships".format(n_nodes, n_rels))

@print_information
def connect_match_data_season_1718():
    df = pd.read_csv("./data/season_files/season1718.csv")
    n_rels = 0
    n_nodes = 0
    for _, row in df.iterrows():
        # NODES
        # Hometeam
        ht = Team.nodes.get(abbreviation=row["Home/Neutral"])
        # Visitor
        vt = Team.nodes.get(abbreviation=row["Visitor/Neutral"])
        # HomeScore
        hs = Score(score=row["PTS.1"]).save()
        # VisitorScore
        vs = Score(score=row["PTS"]).save()
        # Arena
        a = ht.arena.get()
        # Season
        s = Season.get_or_create(
            {"name": "2017/2018"}
        )[0]
        # Date
        d = Date.get_or_create(
            {"datetime": datetime.strptime(row["Date"] + " " + row["Start (ET)"], "%Y-%m-%d %I:%M %p")}
        )[0]
        # Game
        g = Game(
            game_id=row["game_id"],
            game_name=row["game_name"],
            game_type=row["game_type"],
            ot=row["OT"]).save() 
        n_nodes += 1
        
        # RELATIONSHIPS
        # Team -> Score
        ht.scored.connect(hs)
        vt.scored.connect(vs)
        # Score -> Game
        hs.in_game.connect(g)
        vs.in_game.connect(g)
        # Game -> Season
        g.season.connect(s)
        # Game -> Date
        g.date.connect(d)
        # Game -> Arena
        g.arena.connect(a)
        n_rels += 7
    print("created (approx:) {} nodes and {} relationships".format(n_nodes, n_rels))

if __name__ == "__main__":
    # connect to Neo4J
    init_connection()

    # create nodes
    connect_match_data_season_1516()
    connect_match_data_season_1617()
    connect_match_data_season_1718()
