"""
Name: wolwm
Description: Wake-On-LAN Web Manager
"""

import sys
import os
from importlib import metadata
from gevent import monkey

# Perform monkey patching
# monkey.patch_all()

# Project Info
__title__ = "wolwm"
__version__ = "0.1.0"
__description__ = (
    "Wake-On-LAN Web Manager"
)

# Adding the 'wolwm' directory to the python path
sys.path.insert(0, os.path.join(os.getcwd(), "wolwm"))