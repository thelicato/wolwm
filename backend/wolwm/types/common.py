"""
This modules contains all the common Pydantic types
"""

# Local application imports
from wolwm.types.base import CamelModel

class BaseDevice(CamelModel):
    """Class for storing base device data"""

    name: str
    mac: str

class Device(BaseDevice):
    """Class for storing device data"""

    id: str