"""
Module to init the DB setup and export all the db stuff
"""

from wolwm.db import database, models

def init_db():
    """Function to init the db and create needed rows if missing"""

    models.Base.metadata.create_all(bind=database.engine)
