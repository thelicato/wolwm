"""
Service module for waking up devices
"""

# Standard library imports
from datetime import datetime, timedelta

# External library imports
from wakeonlan import send_magic_packet

# Local application imports
from wolwm import types
from wolwm.config import default
from wolwm.db import crud
from wolwm.utils import helper


def wake_device(data: types.api.WakeReq) -> types.api.GenericDataRes:
    """Function to wake a device"""

    device = crud.get_device_by_id(data.device_id) # This function automatically raises an error if the ID is wrong

    # Perform another check on the MAC address (just to be sure)
    if not helper.is_valid_mac(device.mac):
        raise Exception("Invalid MAC Address")
    
    # Get the current datetime
    current_datetime = datetime.now()

    # Calculate the datetime for 10 seconds ago
    datetime_to_compare = current_datetime - timedelta(seconds=default.DEFAULT_SECONDS_BETWEEN_WAKES)

    if device.last_waked > datetime_to_compare:
        raise Exception("Not enough time passed since last wake")

    send_magic_packet(device.mac)
    crud.update_last_wake(data.device_id)
    # Save event on the DB
    crud.add_event(types.enum.EventType.WAKE, f"Wake packet sent to  device '{data.device_id}' (Name: '{device.name}' - MAC: '{device.mac}') ")

    res = types.api.GenericDataRes(msg="Magic packet correctly sent")
    return res