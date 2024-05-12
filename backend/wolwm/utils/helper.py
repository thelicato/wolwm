
                                       


"""
This module contains multiple helper function used throughout the codebase.
"""

# Standard library imports
import os
import re
from pathlib import Path
from uuid import uuid4

# Local application imports
from wolwm.log import logger
from wolwm.config import definitions


def banner(version: str) -> None:
    """Print a beautiful banner"""

    print(
        f"""
     _   _          _ _           _        
    | |_| |__   ___| (_) ___ __ _| |_ ___  
    | __| '_ \ / _ \ | |/ __/ _` | __/ _ \ 
    | |_| | | |  __/ | | (_| (_| | || (_) |
     \__|_| |_|\___|_|_|\___\__,_|\__\___/ 
    
    wolwm v{version}
    """
    )

def generate_id() -> str:
    """Generate a ID"""

    return str(uuid4())

def setup_folders() -> None:
    """Check if the data folder has all the necessary subfolders, otherwise create them"""

    home_folder = Path.home()
    data_folder = os.path.join(home_folder, definitions.DEFAULT_BASE_PATH)
    db_folder = os.path.join(data_folder, definitions.WOLWM_DB_FOLDER)

    if not os.path.isdir(data_folder):
        logger.warning("Data folder missing, creating it...")
        os.mkdir(data_folder)

    if not os.path.isdir(db_folder):
        logger.warning("DB folder missing, creating it...")
        os.mkdir(db_folder)

def is_valid_mac(mac: str) -> bool:
    return bool(re.match(definitions.MAC_ADDRESS_PATTERN, mac))