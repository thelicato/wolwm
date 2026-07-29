"""
Module for '/wake' API endpoints
"""

# External library imports
from fastapi import APIRouter, Request, HTTPException

# Local application imports
from wolwm import services, types
from wolwm.log import logger

router = APIRouter(prefix="/wake")


@router.get("/{device_id}/cooldown", dependencies=[])
def get_wake_cooldown(
    device_id: str,
    request: Request,
) -> types.api.WakeCooldownRes:
    """Return the remaining wake cooldown for a device."""

    try:
        return services.wake.get_wake_cooldown(device_id)
    except Exception as err:
        logger.error(
            f"""Error for {request.method} request at {request.url}
            {str(err)}
            """
        )
        raise HTTPException(
            status_code=400,
            detail="Error while retrieving wake cooldown",
        ) from err


@router.post("", dependencies=[])
def wake_device(data:types.api.WakeReq, request: Request) -> types.api.GenericDataRes:
    """Handle wake device requests"""

    try:
        return services.wake.wake_device(data)
    except Exception as err:
        logger.error(
            f"""Error for {request.method} request at {request.url}
            {str(err)}
            """
        )
        raise HTTPException(
            status_code=400, detail="Error while waking device"
        )
