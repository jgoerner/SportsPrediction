import dateutil.parser
from datetime import datetime
import os
from pathlib import Path
os.chdir("/home/jovyan/work")

import pandas as pd
from utils import print_information, send_request



def height_to_cm(height):
    """Utility function to convert feet/inch to cm
    
    Parameters
    ----------
    height: string,
        height of the player in the format "X\"Y'".

    Returns
    -------
    : float
        height in cm
    """
    
    f, i = map(lambda x: int(x), height.replace("\"", "").split("'"))
    return f*30.48 + i*2.54


def pound_to_kg(pounds, decimals=2):
    """Utility function to convert pounds to kg
    
    Paramters
    ---------
    pounds: int,
        weight in pounds.
    decimals: int,
        number of decimals for retun value.
        
    Returns
    -------
    : float
        weight of the player in kg.
    """
    
    return format(pounds*0.453, ".{}f".format(decimals))


def get_player_template():
    """Generate a prefilled player template
    
    Returns
    -------
    template: dict,
        prefilled player template.
    """
    
    template = {
        "id": None,
        "firstName": None,
        "lastName": None,
        "primaryPosition": None,
        "height": "0\'0",
        "weight": 0,
        "birthDate": "3000-01-01",
        "rookie": None,
        "handedness": {"shoots": None},
        "officialImageSrc": None,
        "drafted": {
            "year": -1,
            "round": -1,
            "roundPick": -1,
            "overallPick": -1
        },
        "externalMappings": [{"id":-1}]
    }
    return template


def unmarshall_player(player_sparse):
    """Unmarshall a MSF player JSON to a proper flat dict
    
    Paramters
    ---------
    player_sparse: dict,
        fetched player from MSF API.

    Returns
    -------
    template: dict,
        flat proper player dict.
    """
    
    # init values
    template = get_player_template()
    delta = {}
    
    # get rid of present but "none" kv pairs
    player = player_sparse.copy()
    for k in player_sparse.keys():
        if player_sparse[k] == None or player_sparse[k] == []:
            player.pop(k) 
    
    # fill template with existing data
    for k in template.keys():
        try:
            delta[k] = player[k]
        except KeyError:
            pass
    template.update(delta)
    
    # rename id
    template["msfID"] = template.pop("id")
    
    # rename handedness
    template["shoots"] = template.pop("handedness")["shoots"]
    
    # rename external mappings
    nbaID = template.pop("externalMappings")[0]["id"]
    if nbaID == None:
        template["nbaID"] = -1 
    else:
        template["nbaID"] = nbaID
    
    # adjust units
    template["height"] = height_to_cm(template["height"])
    template["weight"] = pound_to_kg(template["weight"])
    template["birthDate"] = datetime.strptime(template["birthDate"], "%Y-%m-%d")
    
    # adjust nested draft attributes
    template["draftedYear"] = template["drafted"]["year"]
    template["draftedRound"] = template["drafted"]["round"]
    template["draftedRoundPick"] = template["drafted"]["roundPick"]
    template["draftedOverallPick"] = template["drafted"]["overallPick"]
    template.pop("drafted")
    
    return template


@print_information
def create_players():
    # fetch API
    players = \
        send_request("https://api.mysportsfeeds.com/v2.0/pull/nba/players.json")

    # collcet proper player dicts
    player_list = []
    for idx, p in enumerate(players.get("players")):
        player_list.append(unmarshall_player(p["player"]))
        
    # create & savedataframe
    df = pd.DataFrame.from_records(player_list)  
    df.to_csv("./data/generated/players.csv", index=False)


if __name__ == "__main__":
    if input("Fetch MySportFeeds Player API? (NO/yes)") == "yes":
        p = Path("./data/generated")
        if not p.exists():
            p.mkdir(parents=True)
        create_players()
        print(">> Files can be found under ./data/generated <<")