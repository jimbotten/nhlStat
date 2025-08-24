# Import Required Libraries
import requests
import pandas as pd
import pprint
from datetime import date
import json
import glob

# Top Player Penalty Minutes
df = pd.DataFrame()
for file in glob.glob('games/2024*.json'):
    #print(file)
    with open(f'{file}') as json_file:
        data = json.load(json_file)
    dataGame = pd.json_normalize(data,record_path= ['plays'])
    dataGame['game']=file
    df=pd.concat([df,dataGame])
# df.describe()

# Penalties
# df=df[['typeDescKey','details.xCoord','details.yCoord','details.committedByPlayerId','typeCode','details.duration']].loc[df['typeDescKey']=='penalty']
penaltyColumns = [ 
    'typeDescKey',
    'details.xCoord',
    'details.yCoord',
    'details.committedByPlayerId',
    'details.drawnByPlayerId',
    'typeCode',
    'details.duration',
    'details.descKey',
    'periodDescriptor.number',
    'timeInPeriod'
]
df=df.loc[df['typeDescKey']=='penalty']

# df.groupby(df['details.committedByPlayerId'])
players=pd.read_csv('games/players.csv')
df=df.rename(columns={"details.committedByPlayerId":'playerId'})
df=pd.merge(df,players,on="playerId",how='outer')

df=df.loc[df['teamId']==12]
# df=df.loc[df['details.duration']!=0]
df.dropna(subset=['details.duration'],inplace=True)
penaltyPlayers = df.groupby(['lastName.default','firstName.default'])['details.duration'].sum()
penaltyPlayers = penaltyPlayers.sort_values(ascending=False)

print(penaltyPlayers)

# Top types of penalties that hurricanes perform
penaltyTypes = df.groupby(['details.descKey'])['details.descKey'].count()
penaltyTypes = penaltyTypes.sort_values(ascending=False)
print(penaltyTypes)
# df.info()
# df['details.descKey'].unique()

# Hurricane Penalties by Location
# penaltytype='tripping'

penaltyLocations = df.groupby(['lastName.default']).agg(
    avg_x=('details.xCoord','mean'),
    avg_y=('details.yCoord','mean'),
    std_x=('details.xCoord','std'),
    std_y=('details.yCoord','std'),
    count=('lastName.default','count'),
    duration=('details.duration','sum'))
penaltyLocations = penaltyLocations.sort_values(by='count',ascending=False)
print(penaltyLocations)

# types of records
df["typeDescKey"].unique()
#dataGame.dtypes

# Goals
goals=df[(df["typeDescKey"]=="missed-shot") | (df["typeDescKey"]=="blocked-shot")]
# grouped=goals.groupby('team.name')
goals.head(3)[['timeInPeriod','details.reason']]
#goals[['team.name','coordinates.x','coordinates.y']]
# goals.describe

# GET https://statsapi.web.nhl.com/api/v1/teams | Returns a list of data about
# all teams including their id, venue details, division, conference and franchise information.
# GET https://statsapi.web.nhl.com/api/v1/teams/ID | Returns the same information as above just
# for a single team instead of the entire league.

# Team Modifiers
# Add these to the end of the url
# ?expand=team.roster | Shows roster of active players for the specified team
# ?expand=person.names | Same as above, but gives less info.

baseUrlEn="https://statsapi.web.nhl.com/api/v1/teams/12"
baseUrlEn="https://api-web.nhle.com/v1/roster-season/CAR"
# baseUrlEn="https://api.nhle.com/v1/roster/CAR/now"
response=requests.get(baseUrlEn)
dfroster=pd.json_normalize(response.json())
# print(response)
dfroster
skater=requests.get('https://api.nhle.com/stats/rest/en/skater/summary?8474150')
print(skater)

skater
df.head()
