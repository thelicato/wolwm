"""
Module for '/devices' API endpoints
"""

# External library imports
from fastapi import APIRouter, Request, HTTPException

# Local application imports
from wolwm import services, types
from wolwm.log import logger

router = APIRouter(prefix="/devices")


@router.get("", dependencies=[])
def get_all_devices(request: Request) -> types.api.DevicesRes:
    """Handle get devices requests"""

    try:
        return services.devices.get_devices()
    except Exception as err:
        logger.error(
            f"""Error for {request.method} request at {request.url}
            {str(err)}
            """
        )
        raise HTTPException(
            status_code=400, detail="Error while retrieving devices"
        )
    
@router.post("", dependencies=[])
def add_device(data:types.api.AddDeviceReq, request: Request) -> types.api.GenericDataRes:
    """Handle add device requests"""

    try:
        return services.devices.add_device(data)
    except Exception as err:
        logger.error(
            f"""Error for {request.method} request at {request.url}
            {str(err)}
            """
        )
        raise HTTPException(
            status_code=400, detail="Error while adding device"
        )
    
@router.delete("/{device_id}", dependencies=[])
def delete_device(device_id: str, request: Request) -> types.api.GenericDataRes:
    """Handle delete device requests"""

    try:
        return services.devices.delete_device(device_id)
    except Exception as err:
        logger.error(
            f"""Error for {request.method} request at {request.url}
            {str(err)}
            """
        )
        raise HTTPException(status_code=400, detail="Error while deleting device")
