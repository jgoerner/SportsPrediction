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
    
    "all_games_with_id":
    """
    MATCH 
        (t:Team)-[:SCORED]->(s:Score)-[:IN_GAME]->(g:Game)<-[:IN_GAME]-(s2:Score)<-[:SCORED]-(t2:Team), 
        (sea:Season)
    WHERE 
        (g)-[:TOOK_PLACE_IN]->(sea)
    AND
        right(g.game_name, 3) = t.abbreviation
    RETURN
        g.game_id as game_id,
        sea.name as season,
        t.name as team_home,
        t2.name as team_guest,
        s.score as score_home,
        s2.score as score_guest,
        CASE WHEN s.score > s2.score THEN 1 ELSE 0 END as home_win
    """,
    
    ### Iteration 2 ###
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
    
    "avg_starter_score_preceeding_season":
    """
    MATCH 
        (st:Stat)<-[:HAS_STAT]-(p:Player)-[:STARTS_IN]->(g:Game)-[:TOOK_PLACE_IN]->(sea:Season),
        (t)-[:SCORED]->(sc:Score)-[:IN_GAME]->(g),
        (s:Season)
    WHERE
        LEFT(g.game_type,7) = LEFT(st.season_type,7)
    AND
        (st)-[:IN_SEASON]->(s)
    AND
        (st)-[:IN_TEAM]->(t)
    AND
        s.name = toString(toInt(SUBSTRING(sea.name, 0, 4))-1) + "/" + toString(toInt(SUBSTRING(sea.name, 5))-1)
    RETURN 
        AVG(st.Pts) as avg_pts,
        t.name as team,
        t.abbreviation as team_abbreviation,
        g.game_name as game, 
        g.game_id as game_id,
        g.game_type as game_type,
        sea.name as season,
        s.name as preceeding_season
    ORDER BY sea.name, t.abbreviation
    """,
    
    "avg_starter_complete_stats_preceeding_season":
    """
    MATCH 
        (st:Stat)<-[:HAS_STAT]-(p:Player)-[:STARTS_IN]->(g:Game)-[:TOOK_PLACE_IN]->(sea:Season),
        (t)-[:SCORED]->(sc:Score)-[:IN_GAME]->(g),
        (s:Season)
    WHERE
        LEFT(g.game_type,7) = LEFT(st.season_type,7)
    AND
        (st)-[:IN_SEASON]->(s)
    AND
        (st)-[:IN_TEAM]->(t)
    AND
        s.name = toString(toInt(SUBSTRING(sea.name, 0, 4))-1) + "/" + toString(toInt(SUBSTRING(sea.name, 5))-1)
    RETURN 
        AVG(st.GamesPlayed) as avg_GamesPlayed,
        AVG(st.Fg2PtAtt) as avg_Fg2PtAtt,
        AVG(st.Fg2PtAttPerGame) as avg_Fg2PtAttPerGame,
        AVG(st.Fg2PtMade) as avg_Fg2PtMade,
        AVG(st.Fg2PtMadePerGame) as avg_Fg2PtMadePerGame,
        AVG(st.Fg2PtPct) as avg_Fg2PtPct,
        AVG(st.Fg3PtAtt) as avg_Fg3PtAtt,
        AVG(st.Fg3PtAttPerGame) as avg_Fg3PtAttPerGame,
        AVG(st.Fg3PtMade) as avg_Fg3PtMade,
        AVG(st.Fg3PtMadePerGame) as avg_Fg3PtMadePerGame,
        AVG(st.Fg3PtPct) as avg_Fg3PtPct,
        AVG(st.FgAtt) as avg_FgAtt,
        AVG(st.FgAttPerGame) as avg_FgAttPerGame,
        AVG(st.FgMade) as avg_FgMade,
        AVG(st.FgMadePerGame) as avg_FgMadePerGame,
        AVG(st.FgPct) as avg_FgPct,
        AVG(st.FtAtt) as avg_FtAtt,
        AVG(st.FtAttPerGame) as avg_FtAttPerGame,
        AVG(st.FtMade) as avg_FtMade,
        AVG(st.FtMadePerGame) as avg_FtMadePerGame,
        AVG(st.FtPct) as avg_FtPct,
        AVG(st.OffReb) as avg_OffReb,
        AVG(st.OffRebPerGame) as avg_OffRebPerGame,
        AVG(st.DefReb) as avg_DefReb,
        AVG(st.DefRebPerGame) as avg_DefRebPerGame,
        AVG(st.Reb) as avg_Reb,
        AVG(st.RebPerGame) as avg_RebPerGame,
        AVG(st.Ast) as avg_Ast,
        AVG(st.AstPerGame) as avg_AstPerGame,
        AVG(st.Pts) as avg_Pts,
        AVG(st.PtsPerGame) as avg_PtsPerGame,
        AVG(st.Tov) as avg_Tov,
        AVG(st.TovPerGame) as avg_TovPerGame,
        AVG(st.Stl) as avg_Stl,
        AVG(st.StlPerGame) as avg_StlPerGame,
        AVG(st.Blk) as avg_Blk,
        AVG(st.BlkPerGame) as avg_BlkPerGame,
        AVG(st.BlkAgainst) as avg_BlkAgainst,
        AVG(st.BlkAgainstPerGame) as avg_BlkAgainstPerGame,
        AVG(st.FoulPers) as avg_FoulPers,
        AVG(st.FoulPersPerGame) as avg_FoulPersPerGame,
        AVG(st.PlusMinus) as avg_PlusMinus,
        AVG(st.PlusMinusPerGame) as avg_PlusMinusPerGame,
        AVG(st.MinSeconds) as avg_MinSeconds,
        AVG(st.MinSecondsPerGame) as avg_MinSecondsPerGame,
        t.name as team,
        t.abbreviation as team_abbreviation,
        g.game_name as game, 
        g.game_id as game_id,
        g.game_type as game_type,
        sea.name as season,
        s.name as preceeding_season
    ORDER BY sea.name, t.abbreviation
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
        print("'{feature_name}' is not a proper feature name\n".format(**locals()))
        print("Choose one of the following:\n - " + "\n - ".join([str(k) for k in FEATURES.keys()]))
        return
    
    # derive feature
    init_connection()
    dta, hea = db.cypher_query(FEATURES[feature_name])
    return pd.DataFrame(dta, columns=hea)