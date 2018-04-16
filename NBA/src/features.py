import pandas as pd
from py2neo import Node

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
