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
        db=db,
    )

    tax_service = providers.Factory(
        services.TaxService,
        db=db,
    )

    order_service = providers.Factory(
        services.OrderService,
        db=db,
    )

    loader_service = providers.Factory(
        services.LoaderService,
    )
