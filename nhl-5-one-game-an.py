import pandas as pd

def check_games_by_date(targetDate):

  from datetime import timezone, datetime, timedelta
  #targetDate = '2025-03-15'
  time_window_days = 2  # Example: +/- 2 days

  dfGames = pd.read_csv("_games.csv")
  dfGames['date'] = pd.to_datetime(dfGames['startTime'])

  target_date = pd.to_datetime(targetDate)
  target_date = target_date.replace(tzinfo=timezone.utc)

  # Filter for records within the time window
  df_filtered = dfGames[
    (dfGames['date'] >= target_date - pd.Timedelta(days=time_window_days)) &
    (dfGames['date'] <= target_date + pd.Timedelta(days=time_window_days))
  ]

  #df_filtered.info()
  # Format the 'date' column to month day year
  df_filtered['dateFiltered'] = df_filtered.loc[:,'date'].dt.strftime('%m-%d-%Y')

  print(df_filtered[['gameId','dateFiltered']].head())
  # /()

def find_games(gameidentifier):
	allPlays = pd.read_csv('_plays.csv')
	thisGame = allPlays.loc(allPlays['gameId']==gameidentifier)
	thisGame.info()
	#df_filtered = df.loc[df['Age'] > 25]

target = '2025-03-15'
check_games_by_date(target)
gameid='202421061'
find_games(gameid)

'''
with open('games/2023020303.json') as json_file:
    data = json.load(json_file)
dataGame = pd.json_normalize(data,record_path= ['plays'],max_level=0)
#dataGame = pd.json_normalize(data,record_path=
dataPlayer = pd.json_normalize(data, 'rosterSpots')

dataPlayer=dataPlayer[['playerId','sweaterNumber','positionCode','firstName.default','lastName.default']]
dataPlayer

#dataGame
#dataGame.dtypes
dataGame['typeDescKey'].unique()

dataGame.columns

df=dataGame[(dataGame["typeDescKey"]=='faceoff')]
df[['periodDescriptor','timeInPeriod','details']]
df
basics.dataFrame
#df[["team.name","team.triCode","result.description","about.ordinalNum","about.periodTime","result.strength.code","result.secondaryType"]]
#rslt_df = data[(data['teams.away.team.id'].isin(options)) |
'''