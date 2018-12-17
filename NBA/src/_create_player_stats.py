# Necessary to import custom modules
import os
from pathlib import Path
from uuid import uuid4
os.chdir("/home/jovyan/work/")

from neomodel import (
    IntegerProperty,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
)
import pandas as pd
from tqdm import tqdm

from models import Player, Team, Season, Stat
from utils import init_connection, print_information


@print_information
def create_player_stats():
    # prep misc
    stat_files = {}
    stat_files["regular"] = [f for f in os.listdir("./data/stat-files/") if "regular" in f]
    stat_files["playoff"] = [f for f in os.listdir("./data/stat-files/") if "playoff" in f]
    
    # create stats season by season
    for season_type in stat_files.keys():
        for stat_file in stat_files[season_type]:
            p = Path("data", "stat-files", stat_file)
            df = pd.read_csv(p)
            sea_name = \
                p.name[6:15].replace("-","/") if "regular" in p.name else "{}/{}".format(int(p.name[6:10])-1,p.name[6:10])

            # create an UUID per stat
            df["name"] = [str(uuid4()) for _ in range(len(df))]
            df["season_type"] = season_type

            # process single stat 
            for stat in tqdm(df.to_dict(orient="records"), desc="{sea_name}({season_type})".format(**locals())):
                # fetching/saving nodes
                player_node = Player.nodes.get(msfID=stat.pop("Player ID"))
                team_node = Team.nodes.get(abbreviation=stat.pop("Team Abbr."))
                sea_node = Season.nodes.get(name=sea_name)
                stat_node = Stat(**stat).save()

                # connecting nodes
                stat_node.player.connect(player_node)
                stat_node.team.connect(team_node)
                stat_node.season.connect(sea_node)


if __name__ == "__main__":
    # connect to Neo4J
    init_connection()

    # create nodes
    create_player_stats()