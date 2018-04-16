from py2neo import Graph

def get_connection(user="neo4j", pw="1234"):
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
    g = Graph("bolt://{user}:{pw}@neo4j_container:7687".format(user=user, pw=pw))
    return g
