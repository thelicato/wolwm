"""
Module for custom app logger
"""

# Standard library imports
import logging
from typing import Dict, Any, Callable

# External library imports
import structlog

# Local application imports
from wolwm.config.definitions import BOLD_FORMAT, END_FORMAT


class CustomLogger:
    """App logger as Singleton"""

    logger: logging.Logger = structlog.get_logger()
    verbose_mode: bool = False

    """Implement it as a Singleton"""

    def __new__(cls) -> "CustomLogger":
        if not hasattr(cls, "instance"):
            cls.instance = super(CustomLogger, cls).__new__(cls)
        return cls.instance

    def init(self, verbose_mode: bool) -> None:
        """Set the verbose_mode variable"""

        self.verbose_mode = verbose_mode

    def log(self, msg: str, end: str | None = None) -> None:
        """Normal print"""

        if self.verbose_mode:
            print(msg, flush=True, end=end)

    def bold(self, msg: str, end: str | None = None) -> None:
        """Bold print"""

        print(f"{BOLD_FORMAT}{msg}{END_FORMAT}", flush=True, end=end)

    def info(self, msg: str) -> None:
        """Info msg using structlog"""

        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        """Warning msg using structlog"""
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        """Error msg using structlog"""
        self.logger.error(msg)

    def debug(self, msg: str) -> None:
        """Debug msg using structlog if verbose mode enabled"""
        if self.verbose_mode:
            self.logger.debug(msg)


def add_logger_type(logger_type: str | None) -> Callable:
    """
    Factory function that creates and returns a processor function.
    """

    def add_custom_value(_: Any, __: Any, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processor function that adds a custom value to the event_dict.
        """
        if logger_type:
            event_dict["source"] = logger_type
        return event_dict

    return add_custom_value


def init(verbose_mode: bool, logger_type: str | None = None) -> None:
    """Initialize the logger"""

    structlog.configure(
        processors=[
            add_logger_type(logger_type),  # Include your custom processor here
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.dev.ConsoleRenderer(colors=True, force_colors=True),
        ]
    )
    CustomLogger().init(verbose_mode)


log = CustomLogger().log
bold = CustomLogger().bold
info = CustomLogger().info
warning = CustomLogger().warning
error = CustomLogger().error
debug = CustomLogger().debug