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

    class Config:
        """
        Needed to create the class from SQLAlchemy
        ref: https://docs.pydantic.dev/latest/concepts/models/#arbitrary-class-instances
        """

        from_attributes = True
