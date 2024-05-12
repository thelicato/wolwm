"""
Module to serve the React UI
"""

# External library imports
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, RedirectResponse

# Local application imports
from wolwm.config.definitions import MAIN_DIR

ui = APIRouter()

static_folder = f"{MAIN_DIR}/ui"
assets_folder = f"{static_folder}/assets"


@ui.get("/")
async def default_redirect() -> RedirectResponse:
    """Redirect to /ui for the web interface"""
    return RedirectResponse(url="/ui")


@ui.get("/ui/")
async def serve_index() -> FileResponse:
    """Serve the index file"""
    return FileResponse(f"{static_folder}/index.html")


@ui.get("/ui/favicon.ico")
async def serve_favicon() -> FileResponse:
    """Serve the favicon separately"""
    return FileResponse(f"{static_folder}/favicon.ico")


@ui.get("/ui/logo192.png")
async def serve_logo_small() -> FileResponse:
    """Serve the logo separately"""
    return FileResponse(f"{static_folder}/logo192.png")


@ui.get("/ui/logo512.png")
async def serve_logo_big() -> FileResponse:
    """Serve the logo separately"""
    return FileResponse(f"{static_folder}/logo512.png")


@ui.get("/ui/manifest.json")
async def serve_manifest() -> FileResponse:
    """Serve the manifest separately"""
    return FileResponse(f"{static_folder}/manifest.json")


@ui.route("/ui/robots.txt")
async def serve_robots() -> FileResponse:
    """Serve the robots.txt separately"""
    return FileResponse(f"{static_folder}/robots.txt")


@ui.api_route("/ui/assets/{rest_of_path:path}")
async def serve_assets(_request: Request, rest_of_path: str):
    """Serve the assets dynamically"""
    return FileResponse(f"{assets_folder}/{rest_of_path}")


# Return 'index.html' for everything else
@ui.api_route("/ui/{rest_of_path:path}")
async def catch_all(_request: Request, rest_of_path: str):
    """Serve index for all routes"""
    return FileResponse(f"{static_folder}/index.html")