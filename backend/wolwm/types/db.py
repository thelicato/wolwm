"""
This modules contains all the db Pydantic types
"""

# Standard library imports
from datetime import datetime

# Local application imports
from wolwm.types.common import BaseDevice

class DBDevice(BaseDevice):
    """Class for storing a device in the DB"""

    id: str
    last_waked: datetime
