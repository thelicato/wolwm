"""
Service module for devices management
"""

# Standard library imports
from datetime import datetime

# Local application imports
from wolwm import types
from wolwm.db import crud
from wolwm.utils import helper

def get_devices() -> types.api.DevicesRes:
    """Function to retrieve devices from the db"""

    devices = crud.get_devices()

    res = types.api.DevicesRes(
        devices = [types.common.Device(
            id=d.id,
            name=d.name,
            mac=d.mac
        ) for d in devices]
    )
    return res

def add_device(data: types.api.AddDeviceReq) -> types.api.GenericDataRes:
    """Function to add a new device"""

    if not helper.is_valid_mac(data.mac):
        raise Exception("Invalid MAC Address")
    
    crud.create_device(types.db.DBDevice(
        id=helper.generate_id(),
        name=data.name,
        mac=data.mac,
        last_waked=datetime(1970,1,1)
    ))

    res = types.api.GenericDataRes(msg="Device correctly added")
    return res

def get_device(device_id: str) -> types.common.Device:
    """Function to get a specific device"""

    device = crud.get_device_by_id(device_id)
    res = types.common.Device(
        id=device.id,
        name=device.name,
        mac=device.mac
    )
    return res

def delete_device(device_id: str) -> types.api.GenericDataRes:
    """Function to delete a device"""

    crud.delete_device(device_id)
    res = types.api.GenericDataRes(msg="Device correctly deleted")
    return res