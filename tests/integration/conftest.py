import asyncio
from unittest import mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession

from tom_calculator.application import create_app, create_container


def is_main(config):
    return getattr(config, 'workerinput', {}).get('workerid', 'gw0') == 'gw0'


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def db(request):
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
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    client = TestClient(app)
    yield client
