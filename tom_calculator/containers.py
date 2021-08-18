import logging

from dependency_injector import containers, providers

from tom_calculator.database import Database
from tom_calculator import services

logger = logging.getLogger(__name__)


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    db = providers.Singleton(Database, db_dsn=config.db.async_dsn)

    discount_service = providers.Factory(
        services.DiscountService,
        session=db.provided.session,
    )

    tax_service = providers.Factory(
        services.TaxService,
        session=db.provided.session,
    )

    order_service = providers.Factory(
        services.OrderService,
        session=db.provided.session,
    )

    loader_service = providers.Factory(
        services.LoaderService,
    )
