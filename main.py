from src.nhlStat import config
from src.nhlStat.utils import nhl_data_utils


if __name__ == "__main__":
    nhl_data_utils.write_all_games()
    nhl_data_utils.get_play_by_play()
    nhl_data_utils.write_players()
    nhl_data_utils.write_all_plays()
    
print("Complete")
