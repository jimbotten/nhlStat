import os
import shutil

from nhlStat.utils.config import SUBFOLDER_SOURCE, SUBFOLDER_CURATED


def clear_folders():
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    for folder in [SUBFOLDER_SOURCE, SUBFOLDER_CURATED]:
        folder = os.path.join(base_path, folder)
        if not os.path.exists(folder):
            raise FileNotFoundError(f"The folder path does not exist: {folder}")
        shutil.rmtree(folder)
        os.makedirs(folder)
