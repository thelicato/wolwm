"""
Service module for waking up devices
"""

# Standard library imports
from datetime import datetime

# External library imports
from wakeonlan import send_magic_packet

# Local application imports
from wolwm import types
from wolwm.db import crud
from wolwm.utils import helper


def wake_device(data: types.api.WakeReq) -> types.api.GenericDataRes:
    """Function to wake a device"""

    device = crud.get_device_by_id(data.device_id) # This function automatically raises an error if the ID is wrong

    # Perform another check on the MAC address (just to be sure)
    if not helper.is_valid_mac(device.mac):
        raise Exception("Invalid MAC Address")

    send_magic_packet(device.mac)

    res = types.api.GenericDataRes(msg="Magic packet correctly sent")
    return res