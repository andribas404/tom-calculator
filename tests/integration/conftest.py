import asyncio

import pytest
from fastapi.testclient import TestClient
from tom_calculator.application import create_app, create_container


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    client = TestClient(app)
    yield client


@pytest.fixture(scope='session', autouse=True)
async def create_db():
    container = create_container()
    db = container.db()
    try:
        await db.create_database()
        yield
    finally:
        await db.close()


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
