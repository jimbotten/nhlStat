import pandas as pd

filename = "gamelist.txt"
subfolder = "NHL"
app = pd.read_pickle("NHL/all_plays_and_players.pkl")
df = pd.DataFrame()
print(app.info())

df=app.loc[df['teamId']==12]
df.unique()
# goalDf=df.loc[df['typeDescKey']=='goal']
# goalDf.info()
giveawayPlayers = giveawayDf.groupby(['details.goalieInNetId'])['eventId'].count()
giveawayPlayers = giveawayPlayers.sort_values(ascending=False)

print(giveawayPlayers)

penaltyTypes = df.groupby(['details.descKey'])['details.descKey'].count()
penaltyTypes = penaltyTypes.sort_values(ascending=False)
print(penaltyTypes)
# df.info()
# df['details.descKey'].unique()
   
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

import plotly.express as px
fig = px.scatter(penaltyLocations, x='avg_x', y='avg_y')
fig.show()

 
df.head()
   
import numpy as np
import plotly.graph_objects as go
#remove rows where penalty details are not called out
df = df.loc[df['details.descKey']!='']
#change val of negative x to positive, for half court reports.
for index, row in df.iterrows():
    if row['details.xCoord']<0:
        df.at[index,'details.xCoord']=abs(row['details.xCoord'])
fig = go.Figure(
    data=go.Histogram2d(
    x=df['details.xCoord'],
    y=df['details.yCoord'],
    colorscale='Viridis',
#     colorscale='inferno',
#     colorscale='hot',
#     colorscale='rainbow',
#     colorscale='peach',
    nbinsx=10,
    nbinsy=10))
fig.update_layout(
title = 'Penalty Density',
xaxis_title='x-axis',
yaxis_title='y-axis',
template='plotly_white')
fig.show()