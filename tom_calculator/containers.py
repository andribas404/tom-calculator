import logging

from dependency_injector import containers, providers

from tom_calculator import services
from tom_calculator.database import Database

logger = logging.getLogger(__name__)


class Container(containers.DeclarativeContainer):
    """Container with services."""
    # configuration from config file
    config = providers.Configuration()

    # database in async mode
    db = providers.Singleton(Database, db_dsn=config.db.async_dsn)

    # service for discounts table
    discount_service = providers.Factory(
        services.DiscountService,
        db=db,
    )

    # service for tax table
    tax_service = providers.Factory(
        services.TaxService,
        db=db,
    )

    # service for order processing
    order_service = providers.Factory(
        services.OrderService,
        db=db,
    )

    # service to load data
    loader_service = providers.Factory(
        services.LoaderService,
    )
