# Necessary to import custom modules
import os
os.chdir("/home/jovyan/work")

import pandas as pd

from utils import init_connection, print_information
from models import Player



@print_information
def create_player():
    # prep misc
    n_nodes = 0

    # read and adjust dataframe
    df = pd.read_csv("./data/players.csv")
    df["birthDate"] = pd.to_datetime(df["birthDate"])

    # persist player to graph
    for _, row in df.iterrows():
        Player(**row).save()
        n_nodes += 1
    print("created {n_nodes} nodes ".format(**locals()))


if __name__ == "__main__":
    # connect to Neo4J
    init_connection()

    # create nodes
    create_player()