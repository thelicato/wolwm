"""
Main Entrypoint
"""

# External library imports
import uvicorn
import fastapi
from uvicorn.config import LOGGING_CONFIG
from fastapi.middleware.cors import CORSMiddleware

# External library imports
import typer

# Local application imports
from wolwm import __version__, types, db
from wolwm.log import logger, formatter
from wolwm.utils import helper
from wolwm.api.rest import router
from wolwm.api.static import ui

app = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]})

@app.command()
def run(
        host: str = typer.Option(
            "127.0.0.1", "--host", "-h", help="Host for API server (e.g. '0.0.0.0')"
        ),
        port: int = typer.Option(5000, "--port", "-p", help="Port for API server"),
        verbose: bool = typer.Option(False, "--verbose", "-v", help="Display verbose output"),
        dev: bool = typer.Option(False, "--development", "-dev", help="Start in dev mode")
    ) -> None:
    """This method starts the FastAPI server"""

    # Init logger
    logger.bold(f"Starting on {host}:{port}")
    if verbose:
        logger.bold("Verbose mode on")

    # Check that the needed folders are ok
    helper.setup_folders()

    # Init DB
    db.init_db()

    deploy_mode = types.enum.DeployMode.DEV if dev else types.enum.DeployMode.PROD


    # Starting API
    logger.init(verbose, "server")

    docs_url = None if deploy_mode == types.enum.DeployMode.PROD else "/docs"
    redoc_url = None if deploy_mode == types.enum.DeployMode.PROD else "/redoc"
    openapi_url = None if deploy_mode == types.enum.DeployMode.PROD else "/openapi.json"

    app = fastapi.FastAPI(
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
        lifespan=formatter.configure_logging,
    )

    # Serve static files if in 'production'
    if deploy_mode == types.enum.DeployMode.PROD:
        app.include_router(ui)

    app.include_router(router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Load server
    logger.info(f"wolwm v{__version__} is running on {host}:{port}")
    log_config = LOGGING_CONFIG
    del log_config["loggers"]["uvicorn"]
    uvicorn.run(app, host=host, port=port)

def main() -> None:
    """The main entrypoint"""
    helper.banner(__version__)
    app()


if __name__ == "__main__":
    main()    