import pandas as pd
from datetime import date
import json
import glob
import os
from pathlib import Path

filename = "gamelist.txt"
subfolder = "NHL"

def get_path(sf = subfolder, fn = filename):
	file_path = os.path.join(sf, fn)
	print(f"files are at: {file_path}")
	return file_path

def load_games_data_from_json():
  dfGamesTemp = pd.DataFrame()
  dfGames = pd.DataFrame()
  # load all games
  files = glob.glob(get_path(fn='*.json'))
  for file in files:
    with open(file,'r') as json_file:
      # print(str(file))
      try:
        data = json.load(json_file)
        dfGamesTemp = pd.json_normalize(data, max_level=1)
      except json.JSONDecodeError as e:
        print(f"error on  {file}, which is {e}")

    dfGamesClean = pd.DataFrame()
    # Clean up Games
    dfGamesClean['Id'] = dfGamesTemp['id']
    dfGamesClean['season'] = dfGamesTemp['season']
    dfGamesClean['startTime'] = pd.to_datetime(dfGamesTemp['startTimeUTC'])
    dfGamesClean['homeId'] = dfGamesTemp['homeTeam.id']
    dfGamesClean['homeName'] = dfGamesTemp['homeTeam.abbrev']
    dfGamesClean['awayid'] = dfGamesTemp['awayTeam.id']
    dfGamesClean['awayName'] = dfGamesTemp['awayTeam.abbrev']
    dfGamesClean = dfGamesClean.set_index(['Id'], drop=False)
    dfGamesClean.rename(columns={'Id': 'gameId'}, inplace=True)

    dfGames = pd.concat([dfGamesClean, dfGames])
  return dfGames

def load_players_from_csv():
	dfPlayers=pd.read_csv("_players.csv")
	return dfPlayers

def load_players_data_from_json():
  dfPlayersTemp = pd.DataFrame()
  dfPlayers = pd.DataFrame()
  # load all games
  files = glob.glob(get_path(fn='*.json'))
  for file in files:
    with open(file,'r') as json_file:
      # print(str(file))
      try:
        data = json.load(json_file)
        dfPlayersTemp = pd.json_normalize(data, record_path='rosterSpots') 
      except json.JSONDecodeError as e:
        print(f"error on  {file}, which is {e}")

    dfPlayersClean = pd.DataFrame()
    # Clean up Games
    if dfPlayersTemp.empty != True:
      dfPlayersClean['Id'] = dfPlayersTemp['playerId']
      dfPlayersClean['sweater'] = dfPlayersTemp['sweaterNumber']
      dfPlayersClean['firstName'] = dfPlayersTemp['firstName.default']
      dfPlayersClean['lastName'] = dfPlayersTemp['lastName.default']
      dfPlayersClean['teamId'] = dfPlayersTemp['teamId']
      dfPlayersClean['position'] = dfPlayersTemp['positionCode']
      dfPlayersClean = dfPlayersClean.set_index(['Id'], drop=False)
      dfPlayersClean.rename(columns={'Id': 'playerId'}, inplace=True)
      dfPlayers = pd.concat([dfPlayersClean, dfPlayers])
  #print(dfPlayers.info())
  return dfPlayers

def load_plays_data_from_json(playType):
  dfPlaysTemp = pd.DataFrame()
  dfPlays = pd.DataFrame()
  # load all games
  files = glob.glob(get_path(fn='*.json'))
  for file in files:
    with open(file,'r') as json_file:
      # print(str(file))
      try:
        data = json.load(json_file)
        dfPlaysTemp = pd.json_normalize(data, record_path='plays') 
        dfGamesTemp = pd.json_normalize(data, max_level=1)
      except json.JSONDecodeError as e:
        print(f"error on  {file}, which is {e}")

    dfPlaysClean = pd.DataFrame()
    # Clean up Games
    #print(dfPlaysTemp.info())
    # print(dfPlaysTemp.head(2))
    # print(dfPlaysTemp.count())
    gameId = dfGamesTemp.loc[0,'id']
    if dfPlaysTemp.empty != True:
      #print(dfPlaysTemp.info())
      #break
      dfPlaysClean['playId'] = dfPlaysTemp['eventId']
      dfPlaysClean['time'] = pd.to_timedelta('00:' + dfPlaysTemp['timeInPeriod'])
      dfPlaysClean['period'] = dfPlaysTemp['periodDescriptor.number']	
      dfPlaysClean['homeTeamDefendingSide'] = dfPlaysTemp['homeTeamDefendingSide']
      dfPlaysClean['playType'] = dfPlaysTemp['typeCode']
      dfPlaysClean['playDesc'] = dfPlaysTemp['typeDescKey']
      dfPlaysClean['detailPlayDesc'] = dfPlaysTemp['details.descKey']			      
      dfPlaysClean['playZone'] = dfPlaysTemp['details.zoneCode']
      dfPlaysClean['teamId'] = dfPlaysTemp['details.eventOwnerTeamId']
      dfPlaysClean['playerId'] = dfPlaysTemp['details.committedByPlayerId']			
      dfPlaysClean['xCoord'] = dfPlaysTemp['details.xCoord']
      dfPlaysClean['yCoord'] = dfPlaysTemp['details.yCoord']
      dfPlaysClean['duration'] = dfPlaysTemp['details.duration']
      dfPlaysClean['shootingPlayerId'] = dfPlaysTemp['details.shootingPlayerId']
			
      '''
			
  "details": {
    "xCoord": 84,
    "yCoord": 6,
    "zoneCode": "D",
    "typeCode": "MIN",
    "descKey": "high-sticking",
    "duration": 2,
    "committedByPlayerId": 8476906,
    "drawnByPlayerId": 8482070,
    "eventOwnerTeamId": 12
		'''
         
      #print(f'game id for this file is {gameId}')
      # assign the game column from the game record
      dfPlaysClean['gameId'] = gameId
      # build an index on the game and the play number
      dfPlaysClean['compositeId'] = dfPlaysClean['gameId'] + dfPlaysClean['playId']         
      #print(dfPlaysClean['compositeId'].head())
#      dfPlaysClean = dfPlaysClean.set_index(['gameId','Id'], drop=False)
      dfPlaysClean = dfPlaysClean.set_index(['compositeId'], drop=True)
      # filter out anything that isn't the requested play type'

      if playType != '':
        dfPlaysClean = dfPlaysClean.loc[dfPlaysClean['playDesc'] == playType]
			
      #print(dfPlaysClean['playDesc'].head())
      dfPlays = pd.concat([dfPlaysClean, dfPlays])

  #print(dfPlays.info())
  return dfPlays

def load_all_plays_data_from_json(playType):
  dfPlaysTemp = pd.DataFrame()
  dfPlays = pd.DataFrame()
  # load all games
  files = glob.glob(get_path(fn='*.json'))
  for file in files:
    with open(file,'r') as json_file:
      # print(str(file))
      try:
        data = json.load(json_file)
        dfPlaysTemp = pd.json_normalize(data, record_path='plays') 
        dfGamesTemp = pd.json_normalize(data, max_level=1)
      except json.JSONDecodeError as e:
        print(f"error on  {file}, which is {e}")

    dfPlaysClean = pd.DataFrame()
    # Clean up Games
    gameId = dfGamesTemp.loc[0,'id']
    if dfPlaysTemp.empty != True:
      dfPlays = pd.concat([dfPlaysTemp,dfPlays])
  return dfPlays


dfGames = load_games_data_from_json()
dfPlayers = load_players_data_from_json()
dfGames.sort_values(by='startTime', inplace=True)
dfGames.to_csv('_games.csv')
dfPlayers.to_csv('_players.csv')

''' pt=['period-start', 'faceoff', 'stoppage', 'hit', 'blocked-shot',
       'missed-shot', 'shot-on-goal', 'takeaway', 'giveaway', 'goal',
       'delayed-penalty', 'penalty', 'period-end', 'game-end']
'''
df = load_plays_data_from_json('')
df.to_csv('_plays.csv')
df = load_plays_data_from_json('penalty')
df.to_csv('_plays_penalties.csv')
df = load_plays_data_from_json('goal')
df.to_csv('_plays_goals.csv')
df = load_all_plays_data_from_json('penalty')
df.to_csv('_plays_all_penalties.csv')
df = load_plays_data_from_json('shot-on-goal')
df.to_csv('_plays_shot_on_goal.csv')
df = load_plays_data_from_json('missed-shot')
df.to_csv('_plays_missed_shot.csv')

#fullPenalties = pd.merge(dfPlaysPenalties,dfGames,on='gameId',right_index=True, how='left')
#fullPenalties.to_csv('_penalties.csv')



#print(dfPlaysPenalties.head())
print("complete")
