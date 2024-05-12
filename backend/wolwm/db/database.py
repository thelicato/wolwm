"""
Module for db setup
"""

# Standard library imports
from os import path

# External library imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local application imports
from wolwm.config import default, definitions
from wolwm.utils import helper

data_folder = helper.get_config_var('WOLWM_DATA_FOLDER', default.DEFAULT_WOLWM_FOLDER)
sqlite_storage_path = path.join(data_folder, definitions.WOLWM_SQLITE_STORAGE)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{sqlite_storage_path}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)