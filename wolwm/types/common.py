"""
This modules contains all the common Pydantic types
"""

# Standard library imports
from datetime import datetime

# Local application imports
from wolwm.types.base import CamelModel
from wolwm.types.enum import EventType, ScheduleFrequency

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


class WakeSchedule(CamelModel):
    """A persistent wake-up schedule."""

    id: str
    device_id: str
    next_run_at: datetime | None
    frequency: ScheduleFrequency
    timezone: str
    enabled: bool
    last_run_at: datetime | None = None
    last_error: str | None = None
