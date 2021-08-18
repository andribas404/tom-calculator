"""Application.

Contains 2 fabrics for container and application.
"""
import logging

from fastapi import FastAPI

import tom_calculator
from tom_calculator import endpoints
from tom_calculator.containers import Container
from tom_calculator.util import get_config_path

logger = logging.getLogger(__name__)


def create_container() -> Container:
    """Container factory.

    1. Gets path to configuration file from the environment
    2. Initializes container
    3. Set config from file
    4. Wires package within container (loose coupling)
    """
    config_path = get_config_path()
    container = Container()
    container.config.from_yaml(config_path)
    container.wire(packages=[tom_calculator])
    return container


def create_app() -> FastAPI:
    """Application factory.

    1. Creates container
    2. Initializes FastAPI application
    3. Puts container in it
    4. Adds router with endpoints.
    """
    container = create_container()
    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)

    return app
