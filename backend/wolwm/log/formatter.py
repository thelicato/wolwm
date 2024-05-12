"""
Module for custom structlog formatter
"""

# Standard library imports
import logging
from typing import Dict, AsyncGenerator, Any
from contextlib import asynccontextmanager

# External library imports
import structlog
import fastapi


def get_status_code_name(status_code: int) -> str:
    """Get the name of a status code"""

    # Mapping of HTTP status codes to their names
    status_codes = {
        100: "Continue",
        101: "Switching Protocols",
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        307: "Temporary Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Payload Too Large",
        414: "URI Too Long",
        415: "Unsupported Media Type",
        416: "Range Not Satisfiable",
        417: "Expectation Failed",
        418: "I'm a teapot",  # April Fools' joke in RFC 2324
        422: "Unprocessable Entity",
        426: "Upgrade Required",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
    }

    # Return the name of the status code or a default message
    return status_codes.get(status_code, "Unknown Status Code")


# Define the custom processor
def colorize_http_status(_: Any, __: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add a color to the output line based on the status code"""

    event_list = event_dict["event"].split(" ")
    event_data = " ".join(event_list[:-1])
    status_code = int(event_list[-1])
    if 200 <= status_code < 300:
        color_code = "\033[32m"  # Green
    elif 300 <= status_code < 400:
        color_code = "\033[34m"  # Blue
    elif 400 <= status_code < 590:
        color_code = "\033[31m"  # Red
    else:
        color_code = "\033[0m"  # Reset

    # Apply the color code
    # Reset color at the end
    event_dict["event"] = (
        f"{event_data} \033[0m{color_code}{status_code} {get_status_code_name(status_code)}\033[0m"
    )
    return event_dict


def add_source(_: Any, __: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add 'api' as source"""

    event_dict["source"] = "api"
    return event_dict


@asynccontextmanager
async def configure_logging(_: fastapi.FastAPI) -> AsyncGenerator:
    """Configure the logging"""

    http_formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            colorize_http_status,
            add_source,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.stdlib.add_log_level,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(colors=True, force_colors=True),
        ],
    )
    logger = logging.getLogger("uvicorn.access")
    for handler in logger.handlers:
        handler.setFormatter(http_formatter)
    yield