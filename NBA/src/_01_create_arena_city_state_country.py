from functools import wraps
import os
import time
os.chdir("/home/jovyan/work")

import pandas as pd

from models import Arena
from utils import init_connection, print_information
    

@print_information
def create_arena_nodes(df):
    for _, row in df.drop_duplicates(subset=["stadium"]).iterrows():
        arena = Arena(
            name=row["stadium"],
            capacity=int(row["capacity"].replace(",", "")),
            latitude=row["geo1"],
            longitude=row["geo2"]
        )
        arena.save()

@print_information
def create_city_nodes():
    pass  

@print_information
def create_country_nodes():
    pass
    
@print_information
def create_state_nodes():
    pass

@print_information
def connect_arenas_cities_states_countries():
    pass

if __name__ == "__main__":
    # read underlying data
    df = pd.read_csv("./data/arenas.csv", delimiter=";")
    df.columns = map(lambda x: x.strip(), df.columns)
    
    # connect to Neo4J
    init_connection()

    # create nodes
    create_arena_nodes(df)
    create_city_nodes()
    create_country_nodes()
    create_state_nodes()
    connect_arenas_cities_states_countries()