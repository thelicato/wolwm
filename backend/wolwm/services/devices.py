"""
Service module for devices management
"""

# Local application imports
from wolwm import types
from wolwm.db import crud


def get_devices() -> types.api.DevicesRes:
    
    devices = crud.get_devices()


    res = types.api.DevicesRes(
        devices = [types.common.Device(
            id=d.id,
            name=d.name,
            mac=d.mac
        ) for d in devices]
    )
    return res