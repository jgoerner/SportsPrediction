from dateutil import tz
from datetime import datetime
import io
import os
from pathlib import Path
from time import sleep
os.chdir("/home/jovyan/work")

import arrow
import pandas as pd

from utils import send_request, print_information


# Seasons of interest
SEASONS = [
    "2015-2016-regular",
    "2016-playoff",
    "2016-2017-regular",
    "2017-playoff",
    "2017-2018-regular"
]

DROP_COLS = [
    'LastName',
    'FirstName',
    'Jersey Num',
    'Position',
    'Team ID',
    'Team City',
    'Team Name',
]


def _unmarshall_player_stats(player_stats_raw):
    csv_raw = player_stats_raw.text
    df = pd.read_csv(io.StringIO(csv_raw))
    df.columns = [c[1:] for c in df.columns]
    return df.drop([df.columns[0]] + DROP_COLS, axis=1)


@print_information
def fetch_stats():
    failed_urls = []
    for idx, season in enumerate(SEASONS, 1):
        s = "https://api.mysportsfeeds.com/v2.0/pull/nba/{season}/player_stats_totals.csv".format(season=season)

        req = send_request(s, raw=True)

        if req.status_code == 200:
            print("[{idx:04d}/{total}]: fetched {season}".format(idx=idx, total=len(SEASONS), season=season))
            df = _unmarshall_player_stats(req)
            df.to_csv("./data/generated/stat_files/stats_{season}.csv".format(season=season), index=False)           
        elif req.status_code == 429:
            print("Fetched too much, sleeping for 5 minutes")
            sleep(5*60 + 30)
            req = send_request(s, raw=True)
            print("[{idx:04d}/{total}]: fetched {season}".format(idx=idx, total=len(SEASONS), season=season))
            df = _unmarshall_player_stats(req)
            df.to_csv("./data/generated/stat_files/stats_{season}.csv".format(season=season), index=False)  
        else:
            print("No data for {season}".format(season))
            failed_urls.append(s)

    
if __name__ == "__main__":
    if input("Fetch MySportFeeds Season API? (NO/yes)") == "yes":
        p = Path("./data/generated/stat_files")
        if not p.exists():
            p.mkdir(parents=True)
        fetch_stats()
        print(">> Files can be found under ./data/generated <<")