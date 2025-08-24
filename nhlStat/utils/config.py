from dotenv import load_dotenv
import os

load_dotenv() # This loads variables from .env into the environment

SUBFOLDER_SOURCE = os.getenv("SUBFOLDER_SOURCE", "sourceData")
SUBFOLDER_CURATED = os.getenv("SUBFOLDER_CURATED", "curatedData")
FILENAME_ALL_GAMES = os.getenv("FILENAME_ALL_GAMES", "gamelist.txt")
FILENAME_ALL_PLAYERS = os.getenv("FILENAME_ALL_PLAYERS", "playerlist.txt")
FILENAME_ALL_PLAYS = os.getenv("FILENAME_ALL_PLAYS", "playlist.txt")
FILENAME_ALL_PLAYS_AND_PLAYERS_PKL = os.getenv("FILENAME_ALL_PLAYS_AND_PLAYERS_PKL", "all_plays_and_players.pkl")

BASE_URL = os.getenv("BASE_URL", "https://api.nhle.com/stats/rest/")
BASE_URL_EN = os.getenv("BASE_URL_EN", "https://api.nhle.com/stats/rest/en/")
NEW_URL = os.getenv("NEW_URL", "https://api-web.nhle.com/v1/")

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))