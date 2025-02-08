"""
This modules contains all the Pydantic types for the REST APIs
"""

# Standard library imports
from typing import List

# Local application imports
from wolwm.types.base import CamelModel
from wolwm.types.common import BaseDevice, Device, Event

############################
# Generic and common types #
############################


class GenericDataRes(CamelModel):
    """Generic class for API response"""

    msg: str

#####################################################
# Types for /auth/login and /auth/refresh REST APIs #
#####################################################


class LoginReq(CamelModel):
    """Class for body login request"""

    secret: str


class RefreshReq(CamelModel):
    """Class for token refresh request"""

    refresh_token: str


class LoginOrRefreshRes(CamelModel):
    """Class for login response"""

    access_token: str
    refresh_token: str


###################################
# Types for /auth/logout REST API #
###################################


class LogoutReq(CamelModel):
    """Class for body logout request"""

    access_token: str
    refresh_token: str


###############################
# Types for /devices REST API #
###############################

class DevicesRes(CamelModel):
    """Class for get devices response data"""

    devices: List[Device]

    
AddDeviceReq = BaseDevice


###############################
# Types for /wake REST API #
###############################

class WakeReq(CamelModel):
    """Class for wake device request data"""

    device_id: str


###############################
# Types for /events REST API #
###############################

class EventsRes(CamelModel):
    """Class for get events response data"""

    events: List[Event]