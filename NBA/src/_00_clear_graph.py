from neomodel import clear_neo4j_database, db

from utils import init_connection, print_information


@print_information
def clear_graph():
    init_connection()
    n_nodes = db.cypher_query("MATCH (n) RETURN count(n)")[0][0][0]
    n_relations= db.cypher_query("MATCH ()-[r]->() RETURN count(r)")[0][0][0]
    clear_neo4j_database(db)
    print("deleted {} nodes and {} relationships".format(n_nodes, n_relations))
    
if __name__ == "__main__": 
    if input("Do you really want to clear the graph (NO/yes)") == "yes":
        clear_graph()