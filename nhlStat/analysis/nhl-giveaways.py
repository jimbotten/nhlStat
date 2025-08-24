# Import Required Libraries
import requests
import pandas as pd
import pprint
from datetime import date
import json
import glob

# Load and Process Data
df=pd.read_csv('all_plays.csv')

players=pd.read_csv('games/players.csv')
df=df.rename(columns={"details.playerId":'playerId'})
df=pd.merge(df,players,on="playerId",how='outer')

df=df.loc[df['teamId']==12]
giveawayDf=df.loc[df['typeDescKey']=='giveaway']
# df.info()
