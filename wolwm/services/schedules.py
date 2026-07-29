"""Persistent scheduled wake-up management."""

from __future__ import annotations

import asyncio
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from wolwm import types
from wolwm.db import crud
from wolwm.log import logger
from wolwm.services.wake import wake_device
from wolwm.utils import helper

SCHEDULE_POLL_SECONDS = 5


def utc_now() -> datetime:
    """Return a naive UTC timestamp suitable for the SQLite columns."""

    return datetime.now(UTC).replace(tzinfo=None)


def _zone(timezone_name: str) -> ZoneInfo:
    """Resolve an IANA time zone or raise a user-safe validation error."""

    try:
        return ZoneInfo(timezone_name)
    except (ZoneInfoNotFoundError, ValueError) as err:
        raise ValueError("Invalid time zone") from err


def _as_utc(local_or_aware: datetime, timezone_name: str) -> datetime:
    """Convert a request timestamp to naive UTC."""

    zone = _zone(timezone_name)
    if local_or_aware.tzinfo is None:
        localized = local_or_aware.replace(tzinfo=zone)
    else:
        localized = local_or_aware.astimezone(zone)
    return localized.astimezone(UTC).replace(tzinfo=None)


def get_schedules() -> types.api.WakeSchedulesRes:
    """Retrieve all wake-up schedules."""

    return types.api.WakeSchedulesRes(
        schedules=[
            types.common.WakeSchedule(
                id=schedule.id,
                device_id=schedule.device_id,
                next_run_at=schedule.next_run_at,
                frequency=schedule.frequency,
                timezone=schedule.timezone,
                enabled=schedule.enabled,
                last_run_at=schedule.last_run_at,
                last_error=schedule.last_error,
            )
            for schedule in crud.get_wake_schedules()
        ]
    )


def create_schedule(
    data: types.api.CreateWakeScheduleReq,
) -> types.common.WakeSchedule:
    """Validate and persist a scheduled wake-up."""

    device = crud.get_device_by_id(data.device_id)
    frequency = types.enum.ScheduleFrequency(data.frequency)
    next_run_at = _as_utc(data.scheduled_for, data.timezone)

    if next_run_at <= utc_now():
        raise ValueError("Scheduled time must be in the future")

    schedule = types.db.DBWakeSchedule(
        id=helper.generate_id(),
        device_id=device.id,
        next_run_at=next_run_at,
        frequency=frequency,
        timezone=data.timezone,
        enabled=True,
        last_run_at=None,
        last_error=None,
    )
    crud.create_wake_schedule(schedule)
    crud.add_event(
        types.enum.EventType.SCHEDULE_CREATED,
        (
            f"Wake schedule '{schedule.id}' created for '{device.name}' "
            f"({frequency.value}, {data.timezone})"
        ),
    )
    return types.common.WakeSchedule.model_validate(schedule)


def delete_schedule(schedule_id: str) -> types.api.GenericDataRes:
    """Delete a scheduled wake-up."""

    schedule = crud.get_wake_schedule_by_id(schedule_id)
    crud.delete_wake_schedule(schedule_id)
    crud.add_event(
        types.enum.EventType.SCHEDULE_REMOVED,
        (
            f"Wake schedule '{schedule.id}' removed "
            f"(Device: '{schedule.device_id}')"
        ),
    )
    return types.api.GenericDataRes(msg="Wake schedule correctly deleted")


def _next_run(
    schedule: types.db.DBWakeSchedule,
    after: datetime,
) -> datetime | None:
    """Calculate the next UTC execution while retaining local wall-clock time."""

    frequency = types.enum.ScheduleFrequency(schedule.frequency)
    if frequency == types.enum.ScheduleFrequency.ONCE:
        return None

    zone = _zone(schedule.timezone)
    current_utc = schedule.next_run_at.replace(tzinfo=UTC)
    current_local = current_utc.astimezone(zone)
    local_time = time(
        current_local.hour,
        current_local.minute,
        current_local.second,
        current_local.microsecond,
    )
    next_date = current_local.date()

    while True:
        if frequency == types.enum.ScheduleFrequency.DAILY:
            next_date += timedelta(days=1)
        elif frequency == types.enum.ScheduleFrequency.WEEKLY:
            next_date += timedelta(days=7)
        else:
            next_date = _next_weekday(next_date)

        candidate = datetime.combine(next_date, local_time, tzinfo=zone)
        candidate_utc = candidate.astimezone(UTC).replace(tzinfo=None)
        if candidate_utc > after:
            return candidate_utc


def _next_weekday(current_date: date) -> date:
    """Return the next Monday-Friday date."""

    candidate = current_date + timedelta(days=1)
    while candidate.weekday() >= 5:
        candidate += timedelta(days=1)
    return candidate


def run_due_schedules(now: datetime | None = None) -> int:
    """Claim and execute every schedule due at the supplied UTC time."""

    claimed_at = now or utc_now()
    executed = 0

    for schedule in crud.get_due_wake_schedules(claimed_at):
        next_run_at = _next_run(schedule, claimed_at)
        if not crud.claim_wake_schedule(
            schedule,
            claimed_at=claimed_at,
            next_run_at=next_run_at,
        ):
            continue

        executed += 1
        try:
            wake_device(
                types.api.WakeReq(device_id=schedule.device_id),
                event_type=types.enum.EventType.SCHEDULED_WAKE,
            )
        except Exception as err:
            error = str(err) or err.__class__.__name__
            crud.set_wake_schedule_error(schedule.id, error)
            crud.add_event(
                types.enum.EventType.SCHEDULED_WAKE_FAILED,
                (
                    f"Scheduled wake failed for device '{schedule.device_id}' "
                    f"(Schedule: '{schedule.id}')"
                ),
            )
            logger.error(
                f"Scheduled wake '{schedule.id}' failed: {error}"
            )

    return executed


async def run_scheduler() -> None:
    """Poll persistent schedules until the application shuts down."""

    while True:
        try:
            await asyncio.to_thread(run_due_schedules)
        except asyncio.CancelledError:
            raise
        except Exception as err:
            logger.error(f"Unable to check scheduled wake-ups: {err}")
        await asyncio.sleep(SCHEDULE_POLL_SECONDS)
