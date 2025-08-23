#import requests
import pandas as pd
#import pprint
from datetime import date
import json
import glob
import os
# from jsonpath_ng import parse

## Show a play type
pt=['period-start', 'faceoff', 'stoppage', 'hit', 'blocked-shot',
       'missed-shot', 'shot-on-goal', 'takeaway', 'giveaway', 'goal',
       'delayed-penalty', 'penalty', 'period-end', 'game-end']
playType = 'giveaway'
playType = 'goal'
playType = 'penalty'
playType = 'shot-on-goal'


filename = "gamelist.txt"
subfolder = "NHL"
# subfolder and filename
def get_path(fn, sf="games"):
	file_path = os.path.join(os.getcwd(),sf,fn)
	return file_path

# read data right from the json dump and show it to the console
# find first example in each game file
for file in glob.glob(get_path(fn='*.json')):
    #print(file)
    with open(f'{file}') as json_file:
        data = json.load(json_file)
        dataGame = pd.json_normalize(data,record_path=['plays'])
        dataGame['game']=file
        for play in data['plays']:
            if play['typeDescKey']==playType:                
                print(json.dumps(play,indent=2))
                break
# df.info

