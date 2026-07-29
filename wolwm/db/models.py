"""
Module for DB models
"""

# Standard library imports
from uuid import uuid4

# External library imports
from sqlalchemy import Column, Integer, String, DateTime
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