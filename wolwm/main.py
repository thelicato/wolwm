"""
Main Entrypoint
"""

# Standard library imports
import asyncio
from contextlib import asynccontextmanager, suppress

# External library imports
import fastapi
import typer
import uvicorn
from fastapi.staticfiles import StaticFiles
from uvicorn.config import LOGGING_CONFIG

# Local application imports
from wolwm import __version__, db, services, types
from wolwm.log import logger, formatter
from wolwm.utils import helper
from wolwm.api.rest import router
from wolwm.api.static import UI_STATIC_DIR, ui

app = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@asynccontextmanager
async def application_lifespan(application: fastapi.FastAPI):
    """Initialize storage and run the persistent wake scheduler."""

    helper.setup_folders()
    db.init_db()
    services.schedules.configured_timezone()
    services.wake.configured_cooldown_seconds()

    async with formatter.configure_logging(application):
        scheduler_task = asyncio.create_task(
            services.schedules.run_scheduler(),
            name="wolwm-scheduled-wakes",
        )
        try:
            yield
        finally:
            scheduler_task.cancel()
            with suppress(asyncio.CancelledError):
                await scheduler_task


def create_app(deploy_mode: types.enum.DeployMode) -> fastapi.FastAPI:
    """Create the FastAPI application for development or production."""

    docs_url = None if deploy_mode == types.enum.DeployMode.PROD else "/docs"
    redoc_url = None if deploy_mode == types.enum.DeployMode.PROD else "/redoc"
    openapi_url = None if deploy_mode == types.enum.DeployMode.PROD else "/openapi.json"

    application = fastapi.FastAPI(
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
        lifespan=application_lifespan,
    )

    application.mount(
        "/ui/static",
        StaticFiles(directory=str(UI_STATIC_DIR)),
        name="ui-static",
    )
    application.include_router(ui)
    application.include_router(router)

    @application.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "base-uri 'none'; "
            "font-src 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none'; "
            "img-src 'self'; "
            "manifest-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'"
        )
        response.headers["Permissions-Policy"] = (
            "camera=(), geolocation=(), microphone=()"
        )
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response

    return application


@app.command()
def run(
    host: str = typer.Option(
        "127.0.0.1",
        "--host",
        "-h",
        help="Host for API server (e.g. '0.0.0.0')",
    ),
    port: int = typer.Option(5000, "--port", "-p", help="Port for API server"),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Display verbose output",
    ),
    dev: bool = typer.Option(
        False,
        "--development",
        "-dev",
        help="Start in dev mode",
    ),
) -> None:
    """This method starts the FastAPI server"""

    # Init logger
    logger.bold(f"Starting on {host}:{port}")
    if verbose:
        logger.bold("Verbose mode on")

    deploy_mode = types.enum.DeployMode.DEV if dev else types.enum.DeployMode.PROD

    # Starting API
    logger.init(verbose, "server")

    fastapi_app = create_app(deploy_mode)

    # Load server
    logger.info(f"wolwm v{__version__} is running on {host}:{port}")
    log_config = LOGGING_CONFIG
    del log_config["loggers"]["uvicorn"]
    uvicorn.run(fastapi_app, host=host, port=port)


def main() -> None:
    """The main entrypoint"""
    helper.banner(__version__)
    app()


if __name__ == "__main__":
    main()
