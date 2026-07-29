"""
Service module for waking up devices
"""

# Standard library imports
from datetime import datetime, timedelta
from math import ceil

# External library imports
from wakeonlan import send_magic_packet

# Local application imports
from wolwm import types
from wolwm.config import default
from wolwm.db import crud
from wolwm.utils import helper


def configured_cooldown_seconds() -> int:
    """Return and validate the configured wake cooldown."""

    raw_value = helper.get_config_var(
        "WOLWM_WAKE_COOLDOWN_SECONDS",
        default.DEFAULT_SECONDS_BETWEEN_WAKES,
    )
    try:
        cooldown_seconds = int(raw_value)
    except (TypeError, ValueError) as err:
        raise ValueError(
            "WOLWM_WAKE_COOLDOWN_SECONDS must be a non-negative integer"
        ) from err

    if cooldown_seconds < 0:
        raise ValueError(
            "WOLWM_WAKE_COOLDOWN_SECONDS must be a non-negative integer"
        )
    return cooldown_seconds


def _cooldown_for_device(
    device: types.db.DBDevice,
    current_datetime: datetime,
) -> types.api.WakeCooldownRes:
    """Calculate the remaining cooldown against the device's last wake."""

    available_at = device.last_waked + timedelta(
        seconds=configured_cooldown_seconds()
    )
    remaining_seconds = max(
        0,
        ceil((available_at - current_datetime).total_seconds()),
    )
    return types.api.WakeCooldownRes(
        device_id=device.id,
        can_wake=remaining_seconds == 0,
        remaining_seconds=remaining_seconds,
    )


def get_wake_cooldown(
    device_id: str,
    *,
    current_datetime: datetime | None = None,
) -> types.api.WakeCooldownRes:
    """Return how long a device must wait before another wake request."""

    device = crud.get_device_by_id(device_id)
    return _cooldown_for_device(
        device,
        current_datetime or datetime.now(),
    )


def wake_device(
    data: types.api.WakeReq,
    *,
    event_type: types.enum.EventType = types.enum.EventType.WAKE,
) -> types.api.GenericDataRes:
    """Function to wake a device"""

    device = crud.get_device_by_id(data.device_id) # This function automatically raises an error if the ID is wrong

    # Perform another check on the MAC address (just to be sure)
    if not helper.is_valid_mac(device.mac):
        raise Exception("Invalid MAC Address")
    
    cooldown = _cooldown_for_device(device, datetime.now())
    if not cooldown.can_wake:
        raise Exception("Not enough time passed since last wake")

    send_magic_packet(device.mac)
    crud.update_last_wake(data.device_id)
    # Save event on the DB
    crud.add_event(
        event_type,
        (
            f"Wake packet sent to device '{data.device_id}' "
            f"(Name: '{device.name}' - MAC: '{device.mac}')"
        ),
    )

    res = types.api.GenericDataRes(msg="Magic packet correctly sent")
    return res
