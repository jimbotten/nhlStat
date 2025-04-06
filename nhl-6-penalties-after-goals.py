#import requests
import pandas as pd
# import pprint from datetime 
# import date
# import json
#import glob from jsonpath_ng 
# import parse

## Filter  a play type\n['period-start', 'faceoff', 'stoppage', 'hit', 'blocked-shot',\n       'missed-shot', 'shot-on-goal', 'takeaway', 'giveaway', 'goal',\n       'delayed-penalty', 'penalty', 'period-end', 'game-end']"

df = pd.read_csv('all_plays.csv')
# only certain columns
filtered_df = df[['game', 'eventId', 'sortOrder', 'typeDescKey', 'timeInPeriod', 'periodDescriptor.number']] 

filtered_df['tm']=pd.to_datetime(df['game'].astype(str)[:-2] + " " + df['timeInPeriod']) 
filtered_df.info()
# + df.[['timeInPeriod']].toString()
# only certain types of plays
filtered_df = filtered_df[(filtered_df.typeDescKey.isin(['goal','penalty']))]
fdf = filtered_df.set_index(['game','sortOrder'],drop=False)
#fdf["timestamp"] = fdf['timeInPeriod'].to_timedelta()
fdf=fdf.head(10)
print(fdf.to_string(index=False))
#print(fdf[['tm']].head(10) )
# organize by game
#filtered_df.groupby(filtered_df['game'])
# sort by eventid
#filtered_df.sort_values(by=['game','eventId'])
# filtered_df.head()
# filter on one game
#filtered_df[(filtered_df.game.isin(['2024020254']))]

#filtered_df = filtered_df[['game','typeDescKey', 'timeInPeriod', 'periodDescriptor.number']] 
#print(filtered_df.head(50))

