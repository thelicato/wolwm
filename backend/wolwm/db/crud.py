"""
Module for CRUD db functions
"""

# Standard library imports
from typing import List
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
        sqlite_db.delete(row_to_delete)
        sqlite_db.commit()
