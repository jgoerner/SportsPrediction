import dateparser
import glob
import os
os.chdir("/home/jovyan/work")

import numpy as np
import pandas as pd

from utils import print_information


@print_information
def combine_season_1516_data():
    # read files
    df = pd.concat([pd.read_csv(f) for f in glob.glob('./data/1516/*1516.csv')], ignore_index = True)
    # drop unused columns
    df = df.drop(df.columns[[6, 9]], axis=1)
    # parse date so its format yyyy-mm-dd
    df["Date"] = [dateparser.parse(x) for x in df['Date'] ]
    #sorting by date
    df = df.sort_values(by="Date", axis=0)
    #rename OT column
    df = df.rename(columns={"Unnamed: 7": "OT"})
    #parse OT column to get either 0s or 1s
    df.ix[df["OT"] == "OT", "OT"] = 1
    df.ix[df["OT"] != 1, "OT"] = 0
    # looked up end of the regular season & created the game type column 
    df["game_type"] = ""
    df.ix[df["Date"] > "2016-04-14", "game_type"] = "playoff"
    df.ix[df["Date"] <= "2016-04-13", "game_type"] = "regular_season"
    df.ix[df["Date"] > "2010-04-12", "game_name"] = df["Visitor/Neutral"] + " at " + df["Home/Neutral"]
    df.to_csv("./data/season_files/season1516.csv", sep=',', encoding='utf-8')

@print_information
def combine_season_1617_data():
    # read files
    df = pd.concat([pd.read_csv(f) for f in glob.glob('./data/1617/*1617.csv')], ignore_index = True)
    # drop unused columns
    df = df.drop(df.columns[[6, 9]], axis=1)
    # parse date so its format yyyy-mm-dd
    df["Date"] = [dateparser.parse(x) for x in df['Date'] ]
    #sorting by date
    df = df.sort_values(by="Date", axis=0)
    #rename OT column
    df = df.rename(columns={"Unnamed: 7": "OT"})
    #parse OT column to get either 0s or 1s
    df.ix[df["OT"] == "OT", "OT"] = 1
    df.ix[df["OT"] != 1, "OT"] = 0
    # looked up end of the regular season & created the game type column 
    df["game_type"] = ""
    df.ix[df["Date"] > "2017-04-13", "game_type"] = "playoff"
    df.ix[df["Date"] <= "2017-04-12", "game_type"] = "regular_season"
    df.ix[df["Date"] > "2010-04-12", "game_name"] = df["Visitor/Neutral"] + " at " + df["Home/Neutral"]
    df.to_csv("./data/season_files/season1617.csv", sep=',', encoding='utf-8')

@print_information
def combine_season_1718_data():
    # read files
    df = pd.concat([pd.read_csv(f) for f in glob.glob('./data/1718/*1718.csv')], ignore_index = True)
    # drop unused columns
    df = df.drop(df.columns[[6, 9]], axis=1)
    # parse date so its format yyyy-mm-dd
    df["Date"] = [dateparser.parse(x) for x in df['Date'] ]
    #sorting by date
    df = df.sort_values(by="Date", axis=0)
    #rename OT column
    df = df.rename(columns={"Unnamed: 7": "OT"})
    #parse OT column to get either 0s or 1s
    df.ix[df["OT"] == "OT", "OT"] = 1
    df.ix[df["OT"] != 1, "OT"] = 0
    # looked up end of the regular season & created the game type column 
    df["game_type"] = ""
    df.ix[df["Date"] > "2018-04-12", "game_type"] = "playoff"
    df.ix[df["Date"] <= "2018-04-11", "game_type"] = "regular_season"
    df.ix[df["Date"] > "2017-04-12", "game_name"] = df["Visitor/Neutral"] + " at " + df["Home/Neutral"]
    df.to_csv("./data/season_files/season1718.csv", sep=',', encoding='utf-8')
    
if __name__ == "__main__":
    combine_season_1516_data()
    combine_season_1617_data()
    combine_season_1718_data()