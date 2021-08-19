"""Integration conftest."""
import asyncio
from unittest import mock

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession

from tom_calculator.application import create_app, create_container


def is_main(config):
    """Main is true only for the first worker."""
    return getattr(config, 'workerinput', {}).get('workerid', 'gw0') == 'gw0'


@pytest.fixture(scope='session')
def event_loop():
    """Reassign fixture to the session scope."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def db(request):
    """Populates database with schema."""
    container = create_container()
    db = container.db()
    try:
        if is_main(request.config):
            await db.create_database()
        yield db
    finally:
        await db.close()


@pytest.fixture(autouse=True)
async def session_rollback(db):
    """Session management.

    Данное приспособление(fixture) требуется для изолированного тестирования.
    Позволяет запускать тесты параллельно на одной БД.
    Каждый тест запускается в отдельной сессии, которая создает точку сохранения SAVEPOINT.
    В конце сессии делается откат данных и таким образом БД остается в неизменном виде.
    Для этого пародируется(mock) метод класса Database,
    который является асинхронным контекстным менеджером.
    """
    async with db._engine.connect() as connection:
        async with connection.begin() as trans:
            session = AsyncSession(bind=connection)

            class AsyncCM:
                async def __aenter__(self):
                    return session

                async def __aexit__(self, *args):
                    await session.flush()

                def __await__(self):
                    pass

            @event.listens_for(session.sync_session, 'after_transaction_end')
            def restart_savepoint(session_, transaction):
                if transaction.nested and not transaction._parent.nested:
                    session_.begin_nested()

            async with connection.begin_nested():

                with mock.patch('tom_calculator.database.Database.session') as mocked_session:
                    mocked_session.return_value = AsyncCM()
                    yield

            await trans.rollback()


@pytest.fixture
def app(session_rollback):
    """Application fixture."""
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    """Client fixture."""
    client = TestClient(app)
    yield client


@pytest.fixture
async def async_client(app):
    """Async client."""
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
