import argparse
from src.nhlStat import config
from src.nhlStat.utils import nhl_data_utils


if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="NHL Stats Data Processing")

    # Add the --clean argument
    parser.add_argument(
        "--clean",
        action="store_true",  # This makes it a boolean flag
        help="Run data cleaning process",
    )
    # Add the --collect argument
    parser.add_argument(
        "--collect",
        action="store_true",  # This makes it a boolean flag
        help="Collect data from the web",
    )
    # Add the --showConfig argument
    parser.add_argument(
        "--showConfig",
        action="store_true",  # This makes it a boolean flag
        help="Show config info",
    )
    # Add the --process argument
    parser.add_argument(
        "--process",
        action="store_true",  # This makes it a boolean flag
        help="Run data processing",
    )
    # Add the --debug argument
    parser.add_argument(
        "--debug",
        action="store_true",  # This makes it a boolean flag
        help="include debug messsages",
    )  
    
    # Parse the arguments
    args = parser.parse_args()

    if args.collect:
        # Run the main data retrieval process
        nhl_data_utils.write_all_games()
        nhl_data_utils.get_play_by_play()
        nhl_data_utils.write_players()
        nhl_data_utils.write_all_plays()
    
    if args.process:
        nhl_data_utils.process_games()
        nhl_data_utils.process_players()
        nhl_data_utils.process_plays()

print("Complete")
