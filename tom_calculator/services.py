import asyncio
import logging
from decimal import Decimal
from pathlib import Path
from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide

from tom_calculator.database import TSession
from tom_calculator.util import load_csv

logger = logging.getLogger(__name__)


class ServiceWithSession:
    def __init__(self, session: TSession) -> None:
        self._session = session


class DiscountService(ServiceWithSession):
    """Discount service."""
    async def get_discount_by_amount(self, amount: Decimal) -> int:
        """Get the best discount rate by the given amount."""
        return 0

    async def load_data(self, items: Any) -> None:
        """Load data."""


class TaxService(ServiceWithSession):
    """Tax service."""
    async def get_rate_by_state(self, state_name: str) -> Decimal:
        """Get rate of the given state name."""
        return 0

    async def load_data(self, items: Any) -> None:
        """Load data."""


class OrderService(ServiceWithSession):
    """Order service."""
    discount_service: DiscountService = Provide['discount_service']
    tax_service: TaxService = Provide['tax_service']

    async def create(self, item: dict) -> dict:
        """Create order."""
        async with self._session() as session:
            await session.commit()
        return {}

    async def get(self, item_id: UUID):
        """Get order."""
        async with self._session() as session:
            await session.commit()


class LoaderService:
    """Loader service."""
    discount_service: DiscountService = Provide['discount_service']
    tax_service: TaxService = Provide['tax_service']

    async def load(self, datadir: str) -> None:
        """Load data from datadir."""
        discount_file = Path(datadir) / 'discounts.csv'
        discount_items = await LoaderService.run_blocking_io(load_csv, discount_file)
        await self.discount_service.load_data(discount_items)

        tax_file = Path(datadir) / 'taxes.csv'
        tax_items = await LoaderService.run_blocking_io(load_csv, tax_file)
        await self.tax_service.load_data(tax_items)

    @staticmethod
    async def run_blocking_io(self, func, *args) -> Any:
        """Run blocking I/O in executor."""
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, func, *args)
        return result
