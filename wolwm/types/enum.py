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
    DEVICE_ADDED = "device_added"
    DEVICE_REMOVED = "device_removed"