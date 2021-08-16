from dependency_injector import containers, providers

from tom_calculator.database import Database
from tom_calculator.services import OrderService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    db = providers.Singleton(Database, db_dsn=config.db.async_dsn)

    order_service = providers.Factory(
        OrderService,
        session_factory=db.provided.session,
    )
