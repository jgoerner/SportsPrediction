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
        sea.name as season,
        sum(CASE WHEN s.score > s2.score AND g.game_type = "regular_season" THEN 1 ELSE 0 END) as wins 
    ORDER BY 
        team, season
    """,
    "wins_per_team_per_season_as_home":
    """
    MATCH 
        (t:Team)-[:SCORED]->(s:Score)-[:IN_GAME]->(g:Game)<-[:IN_GAME]-(s2:Score)<-[:SCORED]-(t2:Team), 
        (sea:Season)
    WHERE 
        (g)-[:TOOK_PLACE_IN]->(sea)
    AND
        right(g.game_name, 3) = t.abbreviation
    RETURN 
        t.name as team, 
        sea.name as season,
        sum(CASE WHEN s.score > s2.score AND g.game_type = "regular_season" THEN 1 ELSE 0 END) as wins_as_home
    ORDER BY 
        team, season
    """,
    "wins_per_team_per_season_as_guest":
    """
    MATCH 
        (t:Team)-[:SCORED]->(s:Score)-[:IN_GAME]->(g:Game)<-[:IN_GAME]-(s2:Score)<-[:SCORED]-(t2:Team), 
        (sea:Season)
    WHERE 
        (g)-[:TOOK_PLACE_IN]->(sea)
    AND
        right(g.game_name, 3) = t2.abbreviation
    RETURN 
        t.name as team, 
        sea.name as season,
        sum(CASE WHEN s.score > s2.score AND g.game_type = "regular_season" THEN 1 ELSE 0 END) as wins_as_guest
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
        sea.name as season,
        sum(CASE WHEN s.score < s2.score AND g.game_type = "regular_season" THEN 1 ELSE 0 END) as losses
    ORDER BY 
        team, season
    """,
    "losses_per_team_per_season_as_home":
    """
    MATCH 
        (t:Team)-[:SCORED]->(s:Score)-[:IN_GAME]->(g:Game)<-[:IN_GAME]-(s2:Score)<-[:SCORED]-(t2:Team), 
        (sea:Season)
    WHERE 
        (g)-[:TOOK_PLACE_IN]->(sea)
    AND
        right(g.game_name, 3) = t.abbreviation
    RETURN 
        t.name as team, 
        sea.name as season,
        sum(CASE WHEN s.score < s2.score AND g.game_type = "regular_season" THEN 1 ELSE 0 END) as losses_as_home
    ORDER BY 
        team, season
    """,
    "losses_per_team_per_season_as_guest":
    """
    MATCH 
        (t:Team)-[:SCORED]->(s:Score)-[:IN_GAME]->(g:Game)<-[:IN_GAME]-(s2:Score)<-[:SCORED]-(t2:Team), 
        (sea:Season)
    WHERE 
        (g)-[:TOOK_PLACE_IN]->(sea)
    AND
        right(g.game_name, 3) = t2.abbreviation
    RETURN 
        t.name as team,
        sea.name as season,
        sum(CASE WHEN s.score < s2.score AND g.game_type = "regular_season" THEN 1 ELSE 0 END) as losses_as_guest
    ORDER BY 
        team, season
    """,
    "average_score_margin_regular_season":
    """
    MATCH 
        (t:Team)-[:SCORED]->(s:Score)-[:IN_GAME]->(g:Game)<-[:IN_GAME]-(s2:Score)<-[:SCORED]-(t2:Team), (sea:Season)
    WHERE 
        (g)-[:TOOK_PLACE_IN]->(sea)
    AND
        g.game_type= "regular_season"
    RETURN 
        t.name as team, 
        sea.name as season,
        avg(abs(s.score - s2.score)) as score_margin
    ORDER BY 
        team, season
    """,
    "average_score_margin_regular_season_as_home":
    """
    MATCH 
        (t:Team)-[:SCORED]->(s:Score)-[:IN_GAME]->(g:Game)<-[:IN_GAME]-(s2:Score)<-[:SCORED]-(t2:Team), (sea:Season)
    WHERE 
        (g)-[:TOOK_PLACE_IN]->(sea)
    AND
        g.game_type= "regular_season"
    AND
        right(g.game_name, 3) = t.abbreviation
    RETURN 
        t.name as team,
        sea.name as season,
        avg(abs(s.score - s2.score)) as score_margin_as_home
    ORDER BY 
        team, season
    """,
    "average_score_margin_regular_season_as_guest":
    """
    MATCH 
        (t:Team)-[:SCORED]->(s:Score)-[:IN_GAME]->(g:Game)<-[:IN_GAME]-(s2:Score)<-[:SCORED]-(t2:Team), (sea:Season)
    WHERE 
        (g)-[:TOOK_PLACE_IN]->(sea)
    AND
        g.game_type= "regular_season"
    AND
        right(g.game_name, 3) = t2.abbreviation
    RETURN 
        t.name as team, 
        sea.name as season,
        avg(abs(s.score - s2.score)) as score_margin_as_guest
    ORDER BY 
        team, season
    """,
    "all_games":
    """
    MATCH 
        (t:Team)-[:SCORED]->(s:Score)-[:IN_GAME]->(g:Game)<-[:IN_GAME]-(s2:Score)<-[:SCORED]-(t2:Team), 
        (sea:Season)
    WHERE 
        (g)-[:TOOK_PLACE_IN]->(sea)
    AND
        right(g.game_name, 3) = t.abbreviation
    RETURN
        sea.name as season,
        t.name as team_home,
        t2.name as team_guest,
        s.score as score_home,
        s2.score as score_guest,
        CASE WHEN s.score > s2.score THEN 1 ELSE 0 END as home_win
    """,
    
    #Features Iteration 2
    "list_all_games_with_location": 
    """
    MATCH (t:Team)-[sc:SCORED]->(s:Score)-[ig:IN_GAME]->(g:Game)-[po:PLAYED_ON]->(d:Date), (sea:Season), (a:Arena)
    WHERE 
        (g)-[:TOOK_PLACE_IN]->(sea)
    AND
        (g)-[:LOCATED_IN]->(a)
    RETURN 
        d.datetime as date,
        t.name as team,  
        g.game_id as game_id,
        sea.name as Season,
        a.name as Arenaname,
        a.longitude as long,
        a.latitude as lat
    ORDER BY team, date
    
    """,
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