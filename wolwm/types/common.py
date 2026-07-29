"""
This modules contains all the common Pydantic types
"""

# Standard library imports
from datetime import datetime

# Local application imports
from wolwm.types.base import CamelModel
from wolwm.types.enum import EventType

class BaseDevice(CamelModel):
    """Class for storing base device data"""

    name: str
    mac: str

class Device(BaseDevice):
    """Class for storing device data"""

    id: str

class Event(CamelModel):
    """Class for storing event data"""

    id: str
    event_type: EventType
    event_data: str
    timestamp: datetime