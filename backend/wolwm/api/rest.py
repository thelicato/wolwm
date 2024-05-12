"""
Module to include all the REST API routes
"""

# External library imports
from fastapi import APIRouter, Response as FastResponse

# Local application imports
from wolwm.api import routes

router = APIRouter(prefix="/api/v1")
router.include_router(routes.devices.router)
router.include_router(routes.wake.router)


@router.get("/status")  # Status endpoint
def get_status() -> FastResponse:
    """Dummy endpoint to be sure the app is running"""

    return "Everything is up and running"