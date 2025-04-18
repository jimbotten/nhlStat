import os

 # Global variables
SUBFOLDER_SOURCE = "sourceData"
SUBFOLDER_CURATED = "curatedData"
FILENAME_ALL_GAMES = "gamelist.txt"
FILENAME_ALL_PLAYERS = "playerlist.txt"
FILENAME_ALL_PLAYS = "playlist.txt"
FILENAME_ALL_PLAYS_AND_PLAYERS_PKL = "all_plays_and_players.pkl"

BASE_URL = "https://api.nhle.com/stats/rest/"
BASE_URL_EN = "https://api.nhle.com/stats/rest/en/"
NEW_URL = "https://api-web.nhle.com/v1/"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) # Get the root of the project
