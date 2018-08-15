from functools import wraps
import os
import time
os.chdir("/home/jovyan/work")

import pandas as pd

from models import Arena, City, Country, State
from utils import init_connection, print_information
    

@print_information
def create_arena_nodes(df):
    n_nodes = 0
    for _, row in df.drop_duplicates(subset=["stadium"]).iterrows():
        arena = Arena(
            name=row["stadium"],
            capacity=int(row["capacity"].replace(",", "")),
            latitude=row["geo1"],
            longitude=row["geo2"]
        )
        arena.save()
        n_nodes += 1
    print("created {} nodes".format(n_nodes))

@print_information
def create_city_nodes(df):
    n_nodes = 0
    for _, row in df.drop_duplicates(subset=["city"]).iterrows():
        city = City(name=row["city"])
        city.save()
        n_nodes += 1
    print("created {} nodes".format(n_nodes))


@print_information
def create_state_nodes(df):
    n_nodes = 0
    for _, row in df.drop_duplicates(subset=["state"]).iterrows():
        state = State(name=row["state"])
        state.save()
        n_nodes += 1
    print("created {} nodes".format(n_nodes))

@print_information
def create_country_nodes(df):
    n_nodes = 0
    for _, row in df.drop_duplicates(subset=["country"]).iterrows():
        country = Country(name=row["country"])
        country.save()
        n_nodes += 1
    print("created {} nodes".format(n_nodes))
    
@print_information
def connect_arenas_cities_states_countries(df):
    n_rels = 0
    for _, row in df.drop_duplicates(subset=["stadium"]).iterrows():
        # get entities
        a = Arena.nodes.get(name=row["stadium"])
        ci = City.nodes.get(name=row["city"])
        s = State.nodes.get(name=row["state"])
        co = Country.nodes.get(name=row["country"])

        # create relationships
        a.city.connect(ci)
        ci.state.connect(s)
        s.country.connect(co)
        n_rels += 3
    print("created {} relationships".format(n_rels))

if __name__ == "__main__":
    # read underlying data
    df = pd.read_csv("./data/arenas.csv", delimiter=";")
    df.columns = map(lambda x: x.strip(), df.columns)
    
    # connect to Neo4J
    init_connection()

    # create nodes
    create_arena_nodes(df)
    create_city_nodes(df)
    create_state_nodes(df)
    create_country_nodes(df)
    connect_arenas_cities_states_countries(df)