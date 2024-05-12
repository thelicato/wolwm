"""
Module for CRUD db functions
"""

# Standard library imports
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