"""
Module for DB models
"""

# Standard library imports
from uuid import uuid4

# External library imports
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Device(Base):
    """SQLAlchemy class for devices table"""

    __tablename__ = "devices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String)
    mac = Column(String(17), unique=True)
    last_waked = Column(DateTime)

class Event(Base):
    """SQLAlchemy class for events table"""

    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    event_type = Column(String)
    event_data = Column(String)
    timestamp = Column(DateTime)


class WakeSchedule(Base):
    """SQLAlchemy class for persistent wake-up schedules."""

    __tablename__ = "wake_schedules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    device_id = Column(String(36), nullable=False, index=True)
    next_run_at = Column(DateTime, nullable=True, index=True)
    frequency = Column(String, nullable=False)
    timezone = Column(String, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    last_run_at = Column(DateTime, nullable=True)
    last_error = Column(String, nullable=True)
