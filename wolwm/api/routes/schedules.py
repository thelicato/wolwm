"""REST endpoints for scheduled wake-ups."""

from fastapi import APIRouter, HTTPException, Request

from wolwm import services, types
from wolwm.log import logger

router = APIRouter(prefix="/schedules")


@router.get("")
def get_all_schedules(request: Request) -> types.api.WakeSchedulesRes:
    """Return all persistent wake-up schedules."""

    try:
        return services.schedules.get_schedules()
    except Exception as err:
        logger.error(
            f"Error for {request.method} request at {request.url}: {err}"
        )
        raise HTTPException(
            status_code=400,
            detail="Error while retrieving wake schedules",
        ) from err


@router.post("", status_code=201)
def add_schedule(
    data: types.api.CreateWakeScheduleReq,
    request: Request,
) -> types.common.WakeSchedule:
    """Create a persistent wake-up schedule."""

    try:
        return services.schedules.create_schedule(data)
    except Exception as err:
        logger.error(
            f"Error for {request.method} request at {request.url}: {err}"
        )
        raise HTTPException(
            status_code=400,
            detail="Error while adding wake schedule",
        ) from err


@router.delete("/{schedule_id}")
def delete_schedule(
    schedule_id: str,
    request: Request,
) -> types.api.GenericDataRes:
    """Delete a persistent wake-up schedule."""

    try:
        return services.schedules.delete_schedule(schedule_id)
    except Exception as err:
        logger.error(
            f"Error for {request.method} request at {request.url}: {err}"
        )
        raise HTTPException(
            status_code=400,
            detail="Error while deleting wake schedule",
        ) from err
