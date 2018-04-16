import pandas as pd
from py2neo import Node, Relationship

from utils.neo4j import get_connection as neo_connection
from utils.postgres import get_connection as pg_connection

############### NEO4J ###############
def create_team_triples():
    """Generate Team Nodes"""
    df = pd.read_sql("SELECT * FROM source.teamliste", con=pg_connection())
    g = neo_connection()
    name_col = "Team Name"
    node_type = "Team"

    for _, row in df.iterrows():
        row_dict = row.to_dict()
        name = row_dict.pop(name_col)
        node = Node(node_type, name=name, **row_dict)
        g.create(node)

def create_player_college_triples():
    """Generate (Player)-[STUDIED AT]-(COllEGE) triples"""
    df = pd.read_sql("SELECT * FROM source.spielerliste", con=pg_connection())
    g = neo_connection()
    NA_FILL = "None"
    dct_colleges = {}
    relationships = []
    # create university nodes
    for colleg in df["Colleges"].fillna(NA_FILL).unique():
        dct_colleges[colleg] = Node("College", name=colleg)
    # create player - college relationships
    for _, row in df.fillna(NA_FILL).iterrows():
        player = Node("Player", name=row["Player"])
        colleg_name = row["Colleges"]
        colleg = dct_colleges[colleg_name]
        relationships.append(Relationship(player, "STUDIED AT", colleg))
    # add relationships to the graph
    for rel in relationships:
        g.create(rel)
