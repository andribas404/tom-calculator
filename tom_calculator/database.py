"""SQLAlchemy Database."""
import logging
from asyncio import current_task
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Callable

from sqlalchemy import orm
from sqlalchemy.ext.asyncio import (  # type: ignore[attr-defined]
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)

logger = logging.getLogger(__name__)

Base = orm.declarative_base()

TSession = Callable[..., AbstractAsyncContextManager[orm.Session]]


class Database:
    """Database."""
    def __init__(self, db_dsn: str) -> None:
        """Database initialization.

        1. Creates async engine
        2. Creates async session factory
        3. Makes factory scoped.
        """
        self._engine = create_async_engine(db_dsn, future=True, echo=True)
        self._async_session_factory = orm.sessionmaker(
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            bind=self._engine,
        )
        self._session = async_scoped_session(self._async_session_factory, scopefunc=current_task)

    async def create_database(self) -> None:
        """Create database.

        Populates database with schema recreating all tables.
        """
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def close(self) -> None:
        """Close database."""
        await self._engine.dispose()

    @asynccontextmanager  # type: ignore[arg-type]
    async def session(self) -> TSession:  # type: ignore[misc]
        """Session context manager.

        Creates context with scoped session.
        """
        async with self._session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                logger.exception('Session rollback because of exception')
                await session.rollback()
                raise
            finally:
                await session.close()
