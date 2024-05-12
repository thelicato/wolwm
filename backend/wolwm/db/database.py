"""
Module for db setup
"""

# External library imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local application imports
from wolwm.config import definitions

SQLALCHEMY_DATABASE_URL = f"sqlite:///{definitions.WOLWM_SQLITE_STORAGE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)