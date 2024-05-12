"""
This modules contains the all the static definitions
"""

from pathlib import Path

FILE_PATH = Path(__file__)
MAIN_DIR = FILE_PATH.parent.parent.absolute()

# Common definitions
MAC_ADDRESS_PATTERN=r'^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$'
DEFAULT_BASE_PATH = ".wolwm"
WOLWM_SQLITE_STORAGE = "wolwm.db"

# Colors
SUCCESS_COLOR = "\033[92m"
ERROR_COLOR = "\033[91m"
DEBUG_COLOR = "\033[93m"
BOLD_FORMAT = "\033[1m"
END_FORMAT = "\033[0m"