import pandas as pd 

#pens = pd.read_csv('_plays_all_penalties.csv')
pens = pd.read_csv("_plays_penalties.csv")
players = pd.read_csv('_players.csv') 

# playOwnerId
pens = pens.dropna(subset=['playerId'])
pens=pens.loc[pens['teamId']==12] 
pensWithPlayers = pd.merge(pens,players,on=['playerId'],how='inner')
penaltyPlayers = pens.groupby(['playerId'])['duration'].sum() 
penaltyCount = pens.groupby(['playerId'])['duration'].count()
penaltyPlayers = pd.merge(penaltyPlayers,players,on=['playerId'],how='inner')  
penaltyPlayers = penaltyPlayers.sort_values(by='duration',ascending=False)  
penaltyPlayers.drop_duplicates(inplace=True)

penaltyCount = pd.merge(penaltyCount,players,on=['playerId'],how='inner')  
penaltyCount = penaltyCount.sort_values(by='duration',ascending=False)  
penaltyCount.drop_duplicates(inplace=True)

df=pd.DataFrame()
dfc=pd.DataFrame()
#penaltyPlayers.info()
df['lastName'] = penaltyPlayers['lastName']
df['sum'] = penaltyPlayers['duration']
#print(df.head(20))
dfc['lastName'] = penaltyCount['lastName']
dfc['count'] = penaltyCount['duration']
table = pd.merge(df, dfc,on=['lastName'],how='inner')  
table = table.sort_values(by='sum',ascending=False)  
print(table.head(20))

# pens.info()
penTypes = pens.groupby(['detailPlayDesc'])['duration'].count()
penTypes.sort_values(inplace=True,ascending=False)
penTypes.drop_duplicates(inplace=True)
print(penTypes.head(20)) 
'''	

penaltyTypes = df.groupby(['details.descKey'])['details.descKey'].count() 
penaltyTypes = penaltyTypes.sort_values(ascending=False) 
print(penaltyTypes) 
# df.info() 
# df['details.descKey'].unique()
'''
# penaltytype='tripping'  

penaltyLocations = pensWithPlayers.groupby(['lastName']).agg(     
avg_x=('xCoord','mean'),     
avg_y=('yCoord','mean'),     
std_x=('xCoord','std'),     
std_y=('yCoord','std'),     
count=('lastName','count'),     
duration=('duration','sum')) 
penaltyLocations = penaltyLocations.sort_values(by='count',ascending=False) 
#print(penaltyLocations)
'''
import plotly.express as px 
fig = px.scatter(penaltyLocations, x='avg_x', y='avg_y') 
fig.show() 
'''

## Density Cloud",
import numpy as np 
import plotly.graph_objects as go 
	#remove rows where penalty details are not called out df = df.loc[df['details.descKey']!=''] 
	#change val of negative x to positive, for half court reports. for index, row in 
# pensWithPlayers.info()
for index, row in pensWithPlayers.iterrows():     
	if row['xCoord']<0:         
		pensWithPlayers.at[index,'xCoord']=abs(row['xCoord']) 
		fig = go.Figure(     
		data=go.Histogram2d(     
		x=pensWithPlayers['xCoord'],     
		y=pensWithPlayers['yCoord'],     
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
	