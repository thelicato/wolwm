"""
Module for '/events' API endpoints
"""

# External library imports
from fastapi import APIRouter, Request, HTTPException

# Local application imports
from wolwm import services, types
from wolwm.log import logger

router = APIRouter(prefix="/events")


@router.get("", dependencies=[])
def get_all_events(request: Request) -> types.api.EventsRes:
    """Handle get events requests"""

    try:
        return services.events.get_events()
    except Exception as err:
        logger.error(
            f"""Error for {request.method} request at {request.url}
            {str(err)}
            """
        )
        raise HTTPException(
            status_code=400, detail="Error while retrieving events"
        )