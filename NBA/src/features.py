# Necessary to import custom modules
import os
os.chdir("/home/jovyan/work")

from neomodel import db
import pandas as pd

from src.utils import init_connection

FEATURES = {
    "wins_per_team_per_season": 
    """
    MATCH 
        (t:Team)-[:SCORED]->(s:Score)-[:IN_GAME]->(g:Game)<-[:IN_GAME]-(s2:Score)<-[:SCORED]-(t2:Team), 
        (sea:Season)
    WHERE 
        (g)-[:TOOK_PLACE_IN]->(sea)
    RETURN 
        t.name as team, 
        sum(CASE WHEN s.score > s2.score AND g.game_type = "regular_season" THEN 1 ELSE 0 END) as wins, 
        sea.name as season
    ORDER BY 
        team, season
    """,
    "losses_per_team_per_season": 
    """
    MATCH 
        (t:Team)-[:SCORED]->(s:Score)-[:IN_GAME]->(g:Game)<-[:IN_GAME]-(s2:Score)<-[:SCORED]-(t2:Team), 
        (sea:Season)
    WHERE 
        (g)-[:TOOK_PLACE_IN]->(sea)
    RETURN 
        t.name as team, 
        sum(CASE WHEN s.score < s2.score AND g.game_type = "regular_season" THEN 1 ELSE 0 END) as losses, 
        sea.name as season
    ORDER BY 
        team, season
    """,
    "average_play_marging_regular_season":
    """
    MATCH 
        (t:Team)-[:SCORED]->(s:Score)-[:IN_GAME]->(g:Game)<-[:IN_GAME]-(s2:Score)<-[:SCORED]-(t2:Team), (sea:Season)
    WHERE 
        (g)-[:TOOK_PLACE_IN]->(sea)
    AND
        g.game_type= "regular_season"
    RETURN 
        t.name as team, 
        avg(abs(s.score - s2.score)) as scoreMargin,
        sea.name as season
    ORDER BY 
        team, season
    """
}

def get_feature(feature_name):
    """Extract predefined features from the graph
    
    Parameters
    ----------
    feature_name: str,
        name of the feature

    Returns
    -------
    df: pandas.DataFrame
        features based on predefined cypher query
    """
    # check if feature is valid
    if not feature_name in FEATURES.keys():
        print("{feature_name} is not a proper feature name".format(**locals()))
        return
    
    # derive feature
    init_connection()
    dta, hea = db.cypher_query(FEATURES[feature_name])
    return pd.DataFrame(dta, columns=hea)