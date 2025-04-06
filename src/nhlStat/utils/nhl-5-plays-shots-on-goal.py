# shows shots on goal for a player
search_string = 'Jankowski' # 8476873

import pandas as pd

dfPlayers = pd.read_csv('_players.csv')
player_search = 8476873
first_match = dfPlayers[dfPlayers['lastName'].str.contains(search_string, case=False, na=False)].head(1)
player_search = first_match.iloc[0]['playerId']

df = pd.read_csv('_plays_shot_on_goal.csv')
df = df.dropna(subset=['shootingPlayerId'])

myPlays=df[df['shootingPlayerId']==player_search]
games = pd.read_csv('_games.csv')
all = pd.merge(myPlays,games,on='gameId',how='left')
# print(all.info())
print(all[['startTime','homeName','awayName','xCoord','yCoord']])
