"""
This modules contains all the db Pydantic types
"""

# Standard library imports
from datetime import datetime

# Local application imports
from wolwm.types.common import Device

class DBDevice(Device):
    """Class for storing a device in the DB"""

    last_waked: datetime
