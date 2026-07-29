"""
Module for CRUD db functions
"""

# Standard library imports
from typing import List
from datetime import datetime
from contextlib import contextmanager

# Local application imports
from wolwm import types
from wolwm.db import models, database

@contextmanager
def get_db():
    """Get a SQLite DB instance"""

    sqlite_db = database.SessionLocal()
    try:
        yield sqlite_db
    finally:
        sqlite_db.close()

def create_device(device: types.db.DBDevice) -> None:
    """Save a device on the DB"""

    with get_db() as sqlite_db:
        db_device = models.Device(
            id=device.id,
            name=device.name,
            mac=device.mac,
            last_waked=device.last_waked,
        )
        sqlite_db.add(db_device)
        sqlite_db.commit()
        sqlite_db.refresh(db_device)

def get_devices() -> List[types.db.DBDevice]:
    """Get all the devices from the DB"""

    with get_db() as sqlite_db:
        return [
            types.db.DBDevice.model_validate(item)
            for item in sqlite_db.query(models.Device).all()
        ]
    
def get_device_by_id(device_id: str) -> types.db.DBDevice:
    """Get a device from the DB by its ID"""

    with get_db() as sqlite_db:
        row_to_get = sqlite_db.query(models.Device).filter(models.Device.id == device_id).first()
        if not row_to_get:
            raise Exception("Row not found")
        return types.db.DBDevice.model_validate(row_to_get)


def delete_device(device_id: str) -> None:
    """Delete a device from the DB"""

    with get_db() as sqlite_db:
        row_to_delete = sqlite_db.query(models.Device).filter(models.Device.id == device_id).first()
        if not row_to_delete:
            raise Exception("Row not found")
        sqlite_db.query(models.WakeSchedule).filter(
            models.WakeSchedule.device_id == device_id
        ).delete(synchronize_session=False)
        sqlite_db.delete(row_to_delete)
        sqlite_db.commit()

def update_last_wake(device_id: str) -> None:
    """Update 'last_waked' field for a device"""

    with get_db() as sqlite_db:
        row_to_update = sqlite_db.query(models.Device).filter(models.Device.id == device_id).first()
        if not row_to_update:
            raise Exception("Row not found")
        row_to_update.last_waked = datetime.now()
        sqlite_db.commit()
        sqlite_db.refresh(row_to_update)

def add_event(event_type: types.enum.EventType, event_data: str) -> None:
    """Add new event"""

    with get_db() as sqlite_db:
        db_event = models.Event(
            event_type=event_type,
            event_data=event_data,
            timestamp=datetime.now()
        )
        sqlite_db.add(db_event)
        sqlite_db.commit()
        sqlite_db.refresh(db_event)

def get_events() -> List[types.db.DBEvent]:
    """Get all the events from the DB"""

    with get_db() as sqlite_db:
        return [
            types.db.DBEvent.model_validate(item)
            for item in sqlite_db.query(models.Event).all()
        ]


def create_wake_schedule(schedule: types.db.DBWakeSchedule) -> None:
    """Save a wake-up schedule."""

    with get_db() as sqlite_db:
        db_schedule = models.WakeSchedule(
            id=schedule.id,
            device_id=schedule.device_id,
            next_run_at=schedule.next_run_at,
            frequency=schedule.frequency,
            timezone=schedule.timezone,
            enabled=schedule.enabled,
            last_run_at=schedule.last_run_at,
            last_error=schedule.last_error,
        )
        sqlite_db.add(db_schedule)
        sqlite_db.commit()


def get_wake_schedules() -> List[types.db.DBWakeSchedule]:
    """Get all wake-up schedules, ordered by their next run."""

    with get_db() as sqlite_db:
        rows = (
            sqlite_db.query(models.WakeSchedule)
            .order_by(
                models.WakeSchedule.enabled.desc(),
                models.WakeSchedule.next_run_at.asc(),
            )
            .all()
        )
        return [types.db.DBWakeSchedule.model_validate(item) for item in rows]


def get_wake_schedule_by_id(schedule_id: str) -> types.db.DBWakeSchedule:
    """Get a wake-up schedule by ID."""

    with get_db() as sqlite_db:
        row = (
            sqlite_db.query(models.WakeSchedule)
            .filter(models.WakeSchedule.id == schedule_id)
            .first()
        )
        if not row:
            raise Exception("Row not found")
        return types.db.DBWakeSchedule.model_validate(row)


def delete_wake_schedule(schedule_id: str) -> None:
    """Delete a wake-up schedule."""

    with get_db() as sqlite_db:
        row = (
            sqlite_db.query(models.WakeSchedule)
            .filter(models.WakeSchedule.id == schedule_id)
            .first()
        )
        if not row:
            raise Exception("Row not found")
        sqlite_db.delete(row)
        sqlite_db.commit()


def get_due_wake_schedules(now: datetime) -> List[types.db.DBWakeSchedule]:
    """Get enabled schedules due at or before the supplied UTC timestamp."""

    with get_db() as sqlite_db:
        rows = (
            sqlite_db.query(models.WakeSchedule)
            .filter(
                models.WakeSchedule.enabled.is_(True),
                models.WakeSchedule.next_run_at.is_not(None),
                models.WakeSchedule.next_run_at <= now,
            )
            .order_by(models.WakeSchedule.next_run_at.asc())
            .all()
        )
        return [types.db.DBWakeSchedule.model_validate(item) for item in rows]


def claim_wake_schedule(
    schedule: types.db.DBWakeSchedule,
    *,
    claimed_at: datetime,
    next_run_at: datetime | None,
) -> bool:
    """Atomically claim a due schedule so multiple workers cannot send it twice."""

    with get_db() as sqlite_db:
        updated_rows = (
            sqlite_db.query(models.WakeSchedule)
            .filter(
                models.WakeSchedule.id == schedule.id,
                models.WakeSchedule.enabled.is_(True),
                models.WakeSchedule.next_run_at == schedule.next_run_at,
            )
            .update(
                {
                    models.WakeSchedule.enabled: next_run_at is not None,
                    models.WakeSchedule.next_run_at: next_run_at,
                    models.WakeSchedule.last_run_at: claimed_at,
                    models.WakeSchedule.last_error: None,
                },
                synchronize_session=False,
            )
        )
        sqlite_db.commit()
        return updated_rows == 1


def set_wake_schedule_error(schedule_id: str, error: str) -> None:
    """Store the most recent execution error for a schedule."""

    with get_db() as sqlite_db:
        (
            sqlite_db.query(models.WakeSchedule)
            .filter(models.WakeSchedule.id == schedule_id)
            .update(
                {models.WakeSchedule.last_error: error[:500]},
                synchronize_session=False,
            )
        )
        sqlite_db.commit()
