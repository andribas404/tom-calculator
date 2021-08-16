import logging
from fastapi import FastAPI

from tom_calculator.containers import Container
from tom_calculator import endpoints

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    container = Container()
    container.config.from_yaml('config.yml')
    container.wire(modules=[endpoints])

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)

    return app


app = create_app()
