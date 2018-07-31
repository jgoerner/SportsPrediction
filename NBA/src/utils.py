import os
from neomodel import db

def init_connection():
    """
    Initiates the connection to the Neo4J Docker
    """
    db.set_connection("bolt://{auth}@neo4j:7687".format(auth=os.environ["NEO4J_AUTH"].replace("/", ":")))