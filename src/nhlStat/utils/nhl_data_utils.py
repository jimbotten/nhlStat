import requests
import pandas as pd
import json
import os
import glob

from src.nhlStat import config

def get_allGames():
    """
    Retrieves all games for the specified season and team.

    Returns:
        pandas.DataFrame: A DataFrame containing information about all games.
    """
    homeGames = requests.get(config.BASE_URL_EN + "game?&cayenneExp=season=20242025 and homeTeamId=12 and gameType=02")
    awayGames = requests.get(config.BASE_URL_EN + "game?&cayenneExp=season=20242025 and visitingTeamId=12 and gameType=2")

    data = pd.json_normalize(homeGames.json(), 'data')
    adata = pd.json_normalize(awayGames.json(), 'data')
    allGames = pd.concat([data, adata], ignore_index=True)
    allGames = allGames.sort_values(by=['gameDate']).reset_index(drop=True)
    return allGames

def get_path(sf, fn):
    """
    Constructs the file path for a given SUBFOLDER and FILENAME.

    Args:
        sf (str): The SUBFOLDER name.
        fn (str): The FILENAME.

    Returns:
        str: The full file path.
    """
    file_path = os.path.join(config.PROJECT_ROOT, sf, fn)
    return file_path

def write_all_games():
    """
    Writes the IDs of all games to a file.
    """
    with open(get_path(config.SUBFOLDER, config.FILENAME), 'w') as fp:
        allGames = get_allGames()
        for item in allGames.id:
            fp.write(f"{item}\n")

def get_play_by_play():
    """
    Retrieves and saves play-by-play data for each game.
    """
    with open(get_path(config.SUBFOLDER, config.FILENAME), 'r') as fp:
        games = []
        for line in fp:
            x = line[:-1]
            games.append(x)

    for gameNum in games:
        if os.path.isfile(get_path(config.SUBFOLDER, gameNum + '.json')):
            print(f"{gameNum} already there")
        else:
            print(f"didnt find {gameNum}.json")
            gameRes = requests.get(f"{config.NEW_URL}gamecenter/{gameNum}/play-by-play").json()
            json_formatted_str = json.dumps(gameRes, indent=2)
            with open(get_path(config.SUBFOLDER, gameNum + '.json'), "w") as outfile:
                outfile.write(json_formatted_str)
    print('Completed play_by_plays')

def write_players():
    """
    Builds and saves a CSV file of player information.
    """
    df = pd.DataFrame()
    for file in glob.glob(get_path(config.SUBFOLDER, '*.json')):
        with open(file, 'r') as json_file:
            try:
                data = json.load(json_file)
                dataPlayer = pd.json_normalize(data, 'rosterSpots')
                df = pd.concat([df, dataPlayer], ignore_index=True)
            except json.JSONDecodeError as e:
                print(f"error on  {file}, which is {e}")

    df.sort_values(by='playerId', inplace=True)
    df = df[['playerId', 'teamId', 'sweaterNumber', 'positionCode', 'firstName.default', 'lastName.default']]
    df['fn'] = df['firstName.default'].astype('string')
    df['ln'] = df['lastName.default'].astype('string')
    df['position'] = df['positionCode'].astype('string')
    df.drop('firstName.default', axis=1, inplace=True)
    df.drop('lastName.default', axis=1, inplace=True)
    df.drop('positionCode', axis=1, inplace=True)
    df.rename(columns={"details.playerId": "playerId"}, inplace=True)
    players_df = df.drop_duplicates()

    players_df.set_index('playerId', inplace=True)
    print("About to CSV out")
    players_df.to_csv(get_path(config.SUBFOLDER, 'players.csv'))
    print("Completed csv out")

def write_all_plays():
    """
    Builds and saves a CSV and pickle file of all plays and player information.
    """
    df = pd.DataFrame()
    for file in glob.glob(get_path(config.SUBFOLDER, '*.json')):
        with open(f'{file}', 'r', encoding='utf-8-sig') as json_file:
            try:
                data = json.load(json_file)
                dataPlayer = pd.json_normalize(data, 'plays')
                dataPlayer['game'] = file[file.rfind('\\')+1:-5]
                df = pd.concat([df, dataPlayer], ignore_index=True)
            except json.JSONDecodeError as e:
                print(f"error on  {file}, which is {e}")

    df = df.reset_index(drop=True)
    df.rename(columns={"details.playerId": "playerId"}, inplace=True)

    df.to_csv(get_path(config.SUBFOLDER, 'all_plays.csv'), index=False)
    players_df = pd.read_csv(get_path(config.SUBFOLDER, 'players.csv'))
    players_df.drop_duplicates(inplace=True)
    merged_df = pd.merge(df, players_df, on="playerId", how='left')
    print(merged_df.head())
    print("writing all plays and players pickle")
    merged_df.to_pickle(get_path(config.SUBFOLDER, 'all_plays_and_players.pkl'))
