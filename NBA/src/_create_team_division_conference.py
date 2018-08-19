from functools import wraps
import os
import time
os.chdir("/home/jovyan/work")

import pandas as pd

from models import Conference, Division, Team
from utils import init_connection, print_information


@print_information
def create_teams(df):
    n_nodes = 0
    for _, row in df.iterrows():
        team = Team(
            name=row["team"]
            abbreviation=row["abbreviation"]
            team_id=row["team_id"]
        )
        team.save()
        n_nodes += 1
    print("created {} nodes".format(n_nodes))

@print_information
def create_divisions(df):
    n_nodes = 0
    for _, row in df.drop_duplicates(subset=["division"]).iterrows():
        division = Division(
            name=row["division"]  
        )
        division.save()
        n_nodes += 1
    print("created {} nodes".format(n_nodes))
    
@print_information
def create_conferences(df):
    n_nodes = 0
    for _, row in df.drop_duplicates(subset=["conference"]).iterrows():
        conference = Conference(
            name=row["conference"]
        )
        conference.save()
        n_nodes += 1
    print("created {} nodes".format(n_nodes))        

@print_information
def connect_teams_divisions_conferences(df):
    n_rels = 0
    for _, row in df.iterrows():
        # get entities
        t = Team.nodes.get(name=row["team"])
        d = Division.nodes.get(name=row["division"])
        c = Conference.nodes.get(name=row["conference"])

        # create relationships
        t.division.connect(d)
        d.conference.connect(c)
        n_rels += 2
    print("created {} relationships".format(n_rels))  
    
if __name__ == "__main__":
    # read underlying data
    df = pd.read_csv("./data/msf/teams-divisions-conferences.csv", sep=";")    
    
    # connect to Neo4J
    init_connection()

    # create nodes
    create_teams(df)
    create_divisions(df)
    create_conferences(df)
    connect_teams_divisions_conferences(df)