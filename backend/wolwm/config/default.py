"""
This modules contains the all the default config values
"""
# Standard library imports
import os
from pathlib import Path

# Local application imports
from wolwm.config import definitions


DEFAULT_SECRET="changeme"
DEFAULT_SECONDS_BETWEEN_WAKES=10
DEFAULT_WOLWM_FOLDER=os.path.join(Path.home(), definitions.DEFAULT_BASE_PATH)