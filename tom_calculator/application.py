import logging

from fastapi import FastAPI

import tom_calculator
from tom_calculator import endpoints
from tom_calculator.containers import Container
from tom_calculator.util import get_config_path

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Application factory."""
    config_path = get_config_path()
    container = Container()
    container.config.from_yaml(config_path)
    container.wire(packages=[tom_calculator])

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)

    return app


app = create_app()
