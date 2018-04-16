from py2neo import Graph

def get_connection(user, pw):
    """Create connection to neo4j container

    Parameter
    ---------
    user: string,
        neo4j username
    pw: string,
        neo4j password

    Returns
    -------
    g: py2neo.Graph
        graph hosted in neo4j container
    """
    if not user:
        raise ValueError("Must specify a userame when conecting to Neo4j")
    if not pw:
        raise ValueError("Must specify a password when connecting to Neo4j")
    g = Graph("bolt://{user}:{pw}@neo4j_container:7687".format(user=user, pw=pw))
    return g
