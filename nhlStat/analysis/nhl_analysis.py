import pandas as pd

import json
import glob
from nhlStat.utils.nhl_data_utils import get_path

## Show a play type
pt = [
    "period-start",
    "faceoff",
    "stoppage",
    "hit",
    "blocked-shot",
    "missed-shot",
    "shot-on-goal",
    "takeaway",
    "giveaway",
    "goal",
    "delayed-penalty",
    "penalty",
    "period-end",
    "game-end",
]


def play_review(play_type):
    """
    Read data right from the json dump and show it to the console.
    Find the first example in each game file for the specified play type(s).
    """
    # Ensure play_type is a list for consistent processing
    if isinstance(play_type, str):
        play_type = [play_type]

    if not isinstance(play_type, list):
        raise TypeError("play type can be one of several options: 'period-start', 'faceoff', 'stoppage', 'hit', 'blocked-shot', 'missed-shot', 'shot-on-goal', 'takeaway', 'giveaway', 'goal', 'delayed-penalty', 'penalty', 'period-end', 'game-end'")

    for file in glob.glob(get_path(fn="*.json")):
        with open(f"{file}") as json_file:
            data = json.load(json_file)
            dataGame = pd.json_normalize(data, record_path=["plays"])
            dataGame["game"] = file
            for play in data["plays"]:
                if play["typeDescKey"] in play_type:
                    print(json.dumps(play, indent=2))
                    break
