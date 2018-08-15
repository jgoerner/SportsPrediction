from functools import wraps
import os
import time
os.chdir("/home/jovyan/work")

import pandas as pd

from models import Arena, Team
from utils import init_connection, print_information


@print_information
def connect_teams_arenas(df):
    n_rels = 0
    for _, row in df.iterrows():
        # get entities
        a = Arena.nodes.get(name=row["stadium"])
        t = Team.nodes.get(name=row["home_team"])

        # create relationships
        t.arena.connect(a)
        n_rels += 1
    print("created {} relationships".format(n_rels))  

if __name__ == "__main__":
    # read underlying data
    df = pd.read_csv("./data/arenas.csv", delimiter=";")
    df.columns = map(lambda x: x.strip(), df.columns)
    
    # connect to Neo4J
    init_connection()

    # create nodes
    connect_teams_arenas(df)