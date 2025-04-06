import requests 
import pandas as pd 
import pprint from datetime 
import date 
import json
with open('game.stats.json') as json_file:     
    data = json.load(json_file)
    dataGame = pd.json_normalize(data,record_path= ['liveData','plays','allPlays'])

dataGame["result.event"].unique() 
#dataGame.dtypes

df=dataGame[(dataGame["result.event"]=='Goal') &
  (dataGame["team.triCode"]=='CAR')] 
	df[["team.name","team.triCode","result.description","about.ordinalNum","about.periodTime","result.strength.code","result.secondaryType"]] 
#rslt_df = data[(data['teams.away.team.id'].isin(options))