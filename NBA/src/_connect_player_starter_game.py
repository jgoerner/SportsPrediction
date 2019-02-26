from functools import wraps
import os
import time
os.chdir("/home/jovyan/work")

import pandas as pd
from tqdm import tqdm

from models import Game, Player
from utils import init_connection, print_information


@print_information
def connect_team_starter(df):
    n_rels = 0
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        g = Game.nodes.get(game_id=row["game_id"])
        for p1 in ["p_{:02d}".format(n) for n in list(range(1,6))]:
            Player.nodes.get(msfID=row[p1]).startsIn.connect(g, {"for_team":row["t_1"]})
        for p2 in ["p_{:02d}".format(n) for n in list(range(6,11))]:
            Player.nodes.get(msfID=row[p2]).startsIn.connect(g, {"for_team":row["t_2"]})
        n_rels += 10
    print("created {} relationships".format(n_rels))  


if __name__ == "__main__":
    # read underlying data
    df = pd.read_csv("./data/lineups.csv")
    
    # connect to Neo4J
    init_connection()

    # create nodes
    connect_team_starter(df)