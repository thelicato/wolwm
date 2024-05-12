
                                       


"""
This module contains multiple helper function used throughout the codebase.
"""

# Standard library imports
import os
import re
from uuid import uuid4
from typing import Any

# Local application imports
from wolwm.log import logger
from wolwm.config import default, definitions


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

def get_config_var(config_var: str, default_value: Any) -> Any:
    """Get config var"""
    return os.getenv(config_var, default_value)


def setup_folders() -> None:
    """Check if the data folder has all the necessary subfolders, otherwise create them"""

    data_folder = get_config_var('WOLWM_DATA_FOLDER', default.DEFAULT_WOLWM_FOLDER)

    if not os.path.isdir(data_folder):
        logger.warning("Data folder missing, creating it...")
        os.mkdir(data_folder)

def is_valid_mac(mac: str) -> bool:
    return bool(re.match(definitions.MAC_ADDRESS_PATTERN, mac))