"""
Service module for devices management
"""

# Local application imports
from wolwm import types
from wolwm.db import crud

def get_events() -> types.api.EventsRes:
    """Function to retrieve events from the db"""

    events = crud.get_events()

    res = types.api.EventsRes(
        events = [types.common.Event(
            id=e.id,
            event_type=e.event_type,
            event_data=e.event_data,
            timestamp=e.timestamp
        ) for e in events]
    )
    return res