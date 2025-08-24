import glob
import json
import os
import shutil

import pandas as pd
import requests

import nhlStat.utils.config as conf


def clear_folders():
    for folder in [conf.SUBFOLDER_SOURCE, conf.SUBFOLDER_CURATED]:
        folder = os.path.join(conf.BASE_PATH, folder)
        if not os.path.exists(folder):
            raise FileNotFoundError(f"The folder path does not exist: {folder}")
        shutil.rmtree(folder)
        os.makedirs(folder)


def get_allGames():
    """
    Retrieves all games for the specified season and team.

    Returns:
        pandas.DataFrame: A DataFrame containing information about all games.
    """
    homeGames = requests.get(
        conf.BASE_URL_EN
        + "game?&cayenneExp=season=20242025 and homeTeamId=12 and gameType=02"
    )
    awayGames = requests.get(
        conf.BASE_URL_EN
        + "game?&cayenneExp=season=20242025 and visitingTeamId=12 and gameType=2"
    )

    data = pd.json_normalize(homeGames.json(), "data")
    adata = pd.json_normalize(awayGames.json(), "data")
    allGames = pd.concat([data, adata], ignore_index=True)
    allGames = allGames.sort_values(by=["gameDate"]).reset_index(drop=True)
    return allGames


def get_path(fn, sf=conf.SUBFOLDER_SOURCE):
    """
    Constructs the file path for a given SUBFOLDER and FILENAME.

    Args:
        sf (str): The SUBFOLDER name.
        fn (str): The FILENAME.

    Returns:
        str: The full file path.
    """
    file_path = os.path.join(conf.BASE_PATH, sf, fn)
    return file_path


def write_all_games():
    """
    Writes the IDs of all games to a file.
    """
    with open(get_path(fn=conf.FILENAME_ALL_GAMES), "w") as fp:
        allGames = get_allGames()
        for item in allGames.id:
            fp.write(f"{item}\n")


def get_play_by_play():
    """
    Retrieves and saves play-by-play data for each game.
    """
    with open(get_path(fn=conf.FILENAME_ALL_GAMES), "r") as fp:
        games = []
        for line in fp:
            x = line[:-1]
            games.append(x)

    for gameNum in games:
        if os.path.isfile(get_path(fn=gameNum + ".json")):
            print(f"{gameNum} already there")
        else:
            print(f"didnt find {gameNum}.json")
            gameRes = requests.get(
                f"{conf.NEW_URL}gamecenter/{gameNum}/play-by-play"
            ).json()
            json_formatted_str = json.dumps(gameRes, indent=2)
            with open(get_path(fn=gameNum + ".json"), "w") as outfile:
                outfile.write(json_formatted_str)
    print("Completed play_by_plays")


def write_players():
    """
    Builds and saves a CSV file of player information.
    """
    df = pd.DataFrame()
    for file in glob.glob(get_path(fn="*.json")):
        with open(file, "r") as json_file:
            try:
                data = json.load(json_file)
                dataPlayer = pd.json_normalize(data, "rosterSpots")
                df = pd.concat([df, dataPlayer], ignore_index=True)
            except json.JSONDecodeError as e:
                print(f"error on  {file}, which is {e}")

    df.sort_values(by="playerId", inplace=True)
    df = df[
        [
            "playerId",
            "teamId",
            "sweaterNumber",
            "positionCode",
            "firstName.default",
            "lastName.default",
        ]
    ]
    df["fn"] = df["firstName.default"].astype("string")
    df["ln"] = df["lastName.default"].astype("string")
    df["position"] = df["positionCode"].astype("string")
    df.drop("firstName.default", axis=1, inplace=True)
    df.drop("lastName.default", axis=1, inplace=True)
    df.drop("positionCode", axis=1, inplace=True)
    df.rename(columns={"details.playerId": "playerId"}, inplace=True)
    players_df = df.drop_duplicates()

    players_df.set_index("playerId", inplace=True)
    print("About to CSV out")
    players_df.to_csv(get_path(sf=conf.SUBFOLDER_CURATED, fn=conf.FILENAME_ALL_PLAYERS))
    print("Completed csv out")


def write_all_plays():
    """
    Builds and saves a CSV and pickle file of all plays and player information.
    This function performs the following steps:
    1. Initializes an empty DataFrame to store play data.
    2. Iterates over all JSON files in the specified directory:
        - Reads and parses each JSON file.
        - Normalizes the "plays" data into a DataFrame.
        - Adds a "game" column derived from the file name.
        - Concatenates the data into a single DataFrame.
        - Handles JSON decoding errors gracefully.
    3. Resets the index of the DataFrame and renames columns for consistency.
    4. Saves the DataFrame as a CSV file.
    5. Reads a CSV file containing player information, removes duplicates, and merges it with the plays DataFrame.
    6. Saves the merged DataFrame as a pickle file for future use.
    Note:
    - The function relies on helper functions like `get_path` and configuration constants from `config`.
    - Error handling is implemented for JSON decoding issues.
    """
    df = pd.DataFrame()
    for file in glob.glob(get_path(fn="*.json")):
        with open(f"{file}", "r", encoding="utf-8-sig") as json_file:
            try:
                data = json.load(json_file)
                dataPlayer = pd.json_normalize(data, "plays")
                dataPlayer["game"] = file[file.rfind("\\") + 1 : -5]
                df = pd.concat([df, dataPlayer], ignore_index=True)
            except json.JSONDecodeError as e:
                print(f"error on  {file}, which is {e}")

    df = df.reset_index(drop=True)
    df.rename(columns={"details.playerId": "playerId"}, inplace=True)

    # save all players to a curated csv
    df.to_csv(
        get_path(sf=conf.SUBFOLDER_CURATED, fn=conf.FILENAME_ALL_PLAYS), index=False
    )
    # combine the curated player with the play they performed
    players_df = pd.read_csv(
        get_path(sf=conf.SUBFOLDER_CURATED, fn=conf.FILENAME_ALL_PLAYERS)
    )
    players_df.drop_duplicates(inplace=True)
    merged_df = pd.merge(df, players_df, on="playerId", how="left")
    print(merged_df.head())
    print("writing all plays and players pickle")
    # save as a pickle
    merged_df.to_pickle(
        get_path(sf=conf.SUBFOLDER_CURATED, fn=conf.FILENAME_ALL_PLAYS_AND_PLAYERS_PKL)
    )


def load_games_data_from_json():
    dfGamesTemp = pd.DataFrame()
    dfGames = pd.DataFrame()
    # load all games
    files = glob.glob(get_path(fn="*.json"))
    for file in files:
        with open(file, "r") as json_file:
            # print(str(file))
            try:
                data = json.load(json_file)
                dfGamesTemp = pd.json_normalize(data, max_level=1)
            except json.JSONDecodeError as e:
                print(f"error on  {file}, which is {e}")

        dfGamesClean = pd.DataFrame()
        # Clean up Games
        dfGamesClean["Id"] = dfGamesTemp["id"]
        dfGamesClean["season"] = dfGamesTemp["season"]
        dfGamesClean["startTime"] = pd.to_datetime(dfGamesTemp["startTimeUTC"])
        dfGamesClean["homeId"] = dfGamesTemp["homeTeam.id"]
        dfGamesClean["homeName"] = dfGamesTemp["homeTeam.abbrev"]
        dfGamesClean["awayid"] = dfGamesTemp["awayTeam.id"]
        dfGamesClean["awayName"] = dfGamesTemp["awayTeam.abbrev"]
        dfGamesClean = dfGamesClean.set_index(["Id"], drop=False)
        dfGamesClean.rename(columns={"Id": "gameId"}, inplace=True)

        dfGames = pd.concat([dfGamesClean, dfGames])
    return dfGames


def load_players_from_csv():
    dfPlayers = pd.read_csv("_players.csv")
    return dfPlayers


def load_players_data_from_json():
    dfPlayersTemp = pd.DataFrame()
    dfPlayers = pd.DataFrame()
    # load all games
    files = glob.glob(get_path(fn="*.json"))
    for file in files:
        with open(file, "r") as json_file:
            # print(str(file))
            try:
                data = json.load(json_file)
                dfPlayersTemp = pd.json_normalize(data, record_path="rosterSpots")
            except json.JSONDecodeError as e:
                print(f"error on  {file}, which is {e}")

        dfPlayersClean = pd.DataFrame()
        # Clean up Games
        if dfPlayersTemp.empty != True:
            dfPlayersClean["Id"] = dfPlayersTemp["playerId"]
            dfPlayersClean["sweater"] = dfPlayersTemp["sweaterNumber"]
            dfPlayersClean["firstName"] = dfPlayersTemp["firstName.default"]
            dfPlayersClean["lastName"] = dfPlayersTemp["lastName.default"]
            dfPlayersClean["teamId"] = dfPlayersTemp["teamId"]
            dfPlayersClean["position"] = dfPlayersTemp["positionCode"]
            dfPlayersClean = dfPlayersClean.set_index(["Id"], drop=False)
            dfPlayersClean.rename(columns={"Id": "playerId"}, inplace=True)
            dfPlayers = pd.concat([dfPlayersClean, dfPlayers])
    # print(dfPlayers.info())
    return dfPlayers


def load_plays_data_from_json(playType):
    dfPlaysTemp = pd.DataFrame()
    dfPlays = pd.DataFrame()
    # load all games
    files = glob.glob(get_path(fn="*.json"))
    for file in files:
        with open(file, "r") as json_file:
            # print(str(file))
            try:
                data = json.load(json_file)
                dfPlaysTemp = pd.json_normalize(data, record_path="plays")
                dfGamesTemp = pd.json_normalize(data, max_level=1)
            except json.JSONDecodeError as e:
                print(f"error on  {file}, which is {e}")

        dfPlaysClean = pd.DataFrame()
        # Clean up Games
        # print(dfPlaysTemp.info())
        # print(dfPlaysTemp.head(2))
        # print(dfPlaysTemp.count())
        gameId = dfGamesTemp.loc[0, "id"]
        if dfPlaysTemp.empty != True:
            # print(dfPlaysTemp.info())
            # break
            dfPlaysClean["playId"] = dfPlaysTemp["eventId"]
            dfPlaysClean["time"] = pd.to_timedelta("00:" + dfPlaysTemp["timeInPeriod"])
            dfPlaysClean["period"] = dfPlaysTemp["periodDescriptor.number"]
            dfPlaysClean["homeTeamDefendingSide"] = dfPlaysTemp["homeTeamDefendingSide"]
            dfPlaysClean["playType"] = dfPlaysTemp["typeCode"]
            dfPlaysClean["playDesc"] = dfPlaysTemp["typeDescKey"]
            dfPlaysClean["detailPlayDesc"] = dfPlaysTemp["details.descKey"]
            dfPlaysClean["playZone"] = dfPlaysTemp["details.zoneCode"]
            dfPlaysClean["teamId"] = dfPlaysTemp["details.eventOwnerTeamId"]
            dfPlaysClean["playerId"] = dfPlaysTemp["details.committedByPlayerId"]
            dfPlaysClean["xCoord"] = dfPlaysTemp["details.xCoord"]
            dfPlaysClean["yCoord"] = dfPlaysTemp["details.yCoord"]
            dfPlaysClean["duration"] = dfPlaysTemp["details.duration"]
            dfPlaysClean["shootingPlayerId"] = dfPlaysTemp["details.shootingPlayerId"]

            """
			
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
		"""

            # print(f'game id for this file is {gameId}')
            # assign the game column from the game record
            dfPlaysClean["gameId"] = gameId
            # build an index on the game and the play number
            dfPlaysClean["compositeId"] = (
                dfPlaysClean["gameId"] + dfPlaysClean["playId"]
            )
            # print(dfPlaysClean['compositeId'].head())
            #      dfPlaysClean = dfPlaysClean.set_index(['gameId','Id'], drop=False)
            dfPlaysClean = dfPlaysClean.set_index(["compositeId"], drop=True)
            # filter out anything that isn't the requested play type'

            if playType != "":
                dfPlaysClean = dfPlaysClean.loc[dfPlaysClean["playDesc"] == playType]

            # print(dfPlaysClean['playDesc'].head())
            dfPlays = pd.concat([dfPlaysClean, dfPlays])

    # print(dfPlays.info())
    return dfPlays


def load_all_plays_data_from_json(playType):
    dfPlaysTemp = pd.DataFrame()
    dfPlays = pd.DataFrame()
    # load all games
    files = glob.glob(get_path(fn="*.json"))
    for file in files:
        with open(file, "r") as json_file:
            # print(str(file))
            try:
                data = json.load(json_file)
                dfPlaysTemp = pd.json_normalize(data, record_path="plays")
                dfGamesTemp = pd.json_normalize(data, max_level=1)
            except json.JSONDecodeError as e:
                print(f"error on  {file}, which is {e}")

        dfPlaysClean = pd.DataFrame()
        # Clean up Games
        gameId = dfGamesTemp.loc[0, "id"]
        if dfPlaysTemp.empty != True:
            dfPlays = pd.concat([dfPlaysTemp, dfPlays])
    return dfPlays


def process_games():
    dfGames = load_games_data_from_json()
    dfGames.sort_values(by="startTime", inplace=True)
    dfGames.to_csv(get_path(sf=conf.SUBFOLDER_CURATED, fn="_games.csv"))


def process_players():
    dfPlayers = load_players_data_from_json()
    dfPlayers.to_csv(get_path(sf=conf.SUBFOLDER_CURATED, fn="_players.csv"))


def process_plays():
    df = load_plays_data_from_json("")
    df.to_csv(get_path(sf=conf.SUBFOLDER_CURATED, fn="_plays.csv"))
    df = load_plays_data_from_json("penalty")
    df.to_csv(get_path(sf=conf.SUBFOLDER_CURATED, fn="_plays_penalties.csv"))
    df = load_plays_data_from_json("goal")
    df.to_csv(get_path(sf=conf.SUBFOLDER_CURATED, fn="_plays_goals.csv"))
    df = load_all_plays_data_from_json("penalty")
    df.to_csv(get_path(sf=conf.SUBFOLDER_CURATED, fn="_plays_all_penalties.csv"))
    df = load_plays_data_from_json("shot-on-goal")
    df.to_csv(get_path(sf=conf.SUBFOLDER_CURATED, fn="_plays_shot_on_goal.csv"))
    df = load_plays_data_from_json("missed-shot")
    df.to_csv(get_path(sf=conf.SUBFOLDER_CURATED, fn="_plays_missed_shot.csv"))
