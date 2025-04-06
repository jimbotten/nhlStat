import requests
import pandas as pd
import json
# import appex
import os
import os.path
import glob

filename = "gamelist.txt"
subfolder = "NHL"
# baseurl=\"https://api-web.nhle.com/v1\"
# requests.get(f\"https://api.nhle.com/stats/rest/ping\")
baseUrl="https://api.nhle.com/stats/rest/"
newUrl="https://api-web.nhle.com/v1/"
baseUrlEn="https://api.nhle.com/stats/rest/en/"

def get_allGames():
	homeGames=requests.get(baseUrlEn + "game?&cayenneExp=season=20242025 and homeTeamId=12 and gameType=02")
	# homeGames.json()
	awayGames=requests.get(baseUrlEn + "game?&cayenneExp=season=20242025 and visitingTeamId=12 and gameType=2")
	
	data = pd.json_normalize(homeGames.json(),'data')
	adata = pd.json_normalize(awayGames.json(),'data')
	allGames=pd.concat([data,adata], ignore_index=True)
	allGames=allGames.sort_values(by=['gameDate']).reset_index(drop=True)
	# allGames.head(1)['id']",
	return allGames
			
def get_path(sf, fn):
	file_path = os.path.join(sf, fn)
	#print(f"files are at: {file_path}")
	return file_path

def write_all_games():	
	with open(get_path(subfolder, filename), 'w') as fp:
		allGames = get_allGames()
		for item in allGames.id:
			fp.write(f"{item}\n") 

##### NOW Get all play-by-play data
def get_play_by_play():
	with open(get_path(subfolder, filename), 'r') as fp:	
		games =[]
		for line in fp:
			x = line[:-1]
			games.append(x)
	
	for gameNum in games:
		if os.path.isfile(get_path(subfolder, gameNum+'.json')):
			print(f"{gameNum} already there")
			y=1
		else:
			print(f"didnt find {gameNum}.json")
			gameRes=requests.get(f"{newUrl}gamecenter/{gameNum}/play-by-play").json()
			json_formatted_str = json.dumps(gameRes, indent=2)
			with open(get_path(subfolder, gameNum+'.json'), "w") as outfile:
				outfile.write(json_formatted_str)
	print('Completed play_by_plays')

## build players file
def write_players():
	df = pd.DataFrame()
	for file in glob.glob(get_path(subfolder, '*.json')):
#		print(file)
#		with open(file,'r',encoding='utf-8-sig') as json_file:
		with open(file,'r') as json_file:
			try:
				data = json.load(json_file)
				dataPlayer = pd.json_normalize(data, 'rosterSpots')
				df=pd.concat([df,dataPlayer], ignore_index=True)
			except json.JSONDecodeError as e:
				print(f"error on  {file}, which is {e}")
				
#	print(df.info())
	df.sort_values(by='playerId', inplace=True)
	df=df[['playerId','teamId','sweaterNumber','positionCode','firstName.default','lastName.default']]	
	#df=df.drop_duplicates(subset=None, keep='first', inplace=True)
	df['fn']=df['firstName.default'].astype('string')
	df['ln']=df['lastName.default'].astype('string')
	df['position']=df['positionCode'].astype('string')
	df.drop('firstName.default', axis=1, inplace=True)
	df.drop('lastName.default', axis=1, inplace=True)
	df.drop('positionCode', axis=1, inplace=True)
	df.rename(columns={"details.playerId":"playerId"}, inplace=True)
	print(df.info())
	players_df=df 
	#.drop_duplicates()

	players_df.set_index('playerId', inplace=True)
	df.drop_duplicates(inplace=True)
	print("About to CSV out")
	players_df.to_csv(get_path(subfolder, 'players.csv'))
	print("Completed csv out")

### build all plays
def write_all_plays():
	df=pd.DataFrame()
	for file in glob.glob(get_path(subfolder, '*.json')):
		#print(f"found file: {file}")
		with open(f'{file}','r',encoding='utf-8-sig') as json_file:
			try:
				data = json.load(json_file)
				dataPlayer = pd.json_normalize(data, 'plays')
				# add the file name to the temp DF
				dataPlayer['game'] = file[6:16]
				df=pd.concat([df,dataPlayer], ignore_index=True)
			except json.JSONDecodeError as e:
				print(f"error on  {file}, which is {e}")
	#print(df.info())
	df=df.reset_index(drop=True)
	df.rename(columns={"details.playerId":"playerId"}, inplace=True)
	#df=df.loc[df['teamId']==12]
	#df.unique()
	
	#print("writing all plays to csv")
	df.to_csv(get_path(subfolder, 'all_plays.csv'), index=False)
	#print("wrote all plays to csv")
	players_df = pd.read_csv(get_path(subfolder, 'players.csv'))
	#print(df.info())
	players_df.drop_duplicates()
	#print(players_df.info())
	#print(df.shape)
	merged_df=pd.merge(df,players_df,on="playerId",how='left')
	#print(merged_df.shape)
	print(merged_df.head())
	print("writing all plays and players pickle")
	merged_df.to_pickle(get_path(subfolder, 'all_plays_and_players.pkl'))
	#merged_df.info()

write_all_games()
get_play_by_play()
write_players()
write_all_plays()
print("Complete")
