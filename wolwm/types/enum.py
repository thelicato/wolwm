"""
This modules contains all the Pydantic types for most of the enums in the codebase
"""

from enum import Enum

class DeployMode(str, Enum):
    """Enum class for deploy modes"""

    DEV = "development"
    PROD = "production"

class EventType(str, Enum):
    """Enum class for event types"""

    WAKE = "wake"
    SCHEDULED_WAKE = "scheduled_wake"
    SCHEDULED_WAKE_FAILED = "scheduled_wake_failed"
    SCHEDULE_CREATED = "schedule_created"
    SCHEDULE_REMOVED = "schedule_removed"
    DEVICE_ADDED = "device_added"
    DEVICE_REMOVED = "device_removed"


class ScheduleFrequency(str, Enum):
    """Supported recurrence rules for scheduled wake-ups."""

    ONCE = "once"
    DAILY = "daily"
    WEEKDAYS = "weekdays"
    WEEKLY = "weekly"
