from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    def __repr__(self) -> str:
        """Repr function."""
        attrs = ','.join([
            f'{key}={getattr(self, key)}'
            for key in self.__mapper__.c.keys()
        ])
        return f'{self.__class__.__module__}.{self.__class__.__qualname__}({attrs})'


class Database:

    def __init__(self, db_dsn: str) -> None:
        self._engine = create_engine(db_dsn, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[orm.Session]]:
        session: orm.Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()
