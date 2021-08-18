import asyncio
import logging
from decimal import Decimal
from pathlib import Path
from typing import Any, Optional
from uuid import UUID

import sqlalchemy as sa
from dependency_injector.wiring import Provide
from fastapi.encoders import jsonable_encoder
from sqlalchemy.future import select

from tom_calculator.database import TSession
from tom_calculator.models import Discount, Order, Tax, TBase
from tom_calculator.schemas import CalculatorIn
from tom_calculator.util import load_csv, round_down, round_up

logger = logging.getLogger(__name__)


class ServiceWithSession:
    model: Optional[TBase] = None

    def __init__(self, session: TSession) -> None:
        self._session = session

    async def is_empty(self) -> bool:
        """Check that table is empty."""
        stmt = (
            select(
                sa.func.count(),
            )
            .select_from(self.model)
        )
        async with self._session() as session:
            res = await session.execute(stmt)
        is_empty = not res.scalar()
        return is_empty

    async def load_data(self, items: Any) -> None:
        """Load data."""
        stmt = self.model.__table__.insert()
        async with self._session() as session:
            await session.execute(stmt, items)
            await session.commit()


class DiscountService(ServiceWithSession):
    """Discount service."""
    model = Discount

    async def get_discount_rate_by_amount(self, amount: Decimal) -> int:
        """Get the best discount rate by the given amount."""
        stmt = (
            select(
                sa.func.max(Discount.rate),
            )
            .filter(Discount.amount <= amount)
        )
        async with self._session() as session:
            res = await session.execute(stmt)
        discount_rate = res.scalar() or 0
        return discount_rate


class TaxService(ServiceWithSession):
    """Tax service."""
    model = Tax

    async def get_tax_rate_by_state(self, state_name: str) -> Decimal:
        """Get Tax rate of the given state name."""
        stmt = (
            select(
                Tax.rate,
            )
            .filter(Tax.state_name == state_name)
        )
        async with self._session() as session:
            res = await session.execute(stmt)
        rate = res.scalar()
        if rate is None:
            raise TaxNotFoundError(state_name)
        return rate


class OrderService(ServiceWithSession):
    """Order service."""
    model = Order

    discount_service: DiscountService = Provide['discount_service']
    tax_service: TaxService = Provide['tax_service']

    async def create(self, item: CalculatorIn) -> Any:
        """Create order."""
        amount = 0
        for row in item.items:
            amount += row.quantity * row.price
        discount_rate = await self.discount_service.get_discount_rate_by_amount(amount)
        discount = round_down(amount * discount_rate / 100)
        after_discount = amount - discount
        tax_rate = await self.tax_service.get_tax_rate_by_state(item.state_name)
        tax = round_up(after_discount * tax_rate / 100)
        total = after_discount - tax
        order_item = Order(
            amount=amount,
            after_discount=after_discount,
            tax=tax,
            total=total,
        )

        async with self._session() as session:
            session.add(order_item)
            await session.commit()
        order_item_data = jsonable_encoder(order_item)
        return order_item_data

    async def get(self, item_id: UUID) -> Any:
        """Get order."""
        item_id_str = str(item_id)
        stmt = (
            select(
                Order,
            )
            .filter(Order.id == item_id_str)
        )
        async with self._session() as session:
            res = await session.execute(stmt)
        item = res.scalar()
        if item is None:
            raise OrderNotFoundError(item_id)
        item_data = jsonable_encoder(item)
        return item_data


class LoaderService:
    """Loader service."""
    discount_service: DiscountService = Provide['discount_service']
    tax_service: TaxService = Provide['tax_service']

    async def load(self, datadir: str) -> None:
        """Load data from datadir."""
        is_empty = await self.discount_service.is_empty()
        if is_empty:
            discount_file = Path(datadir) / 'discounts.csv'
            discount_items = await LoaderService.run_blocking_io(load_csv, discount_file)
            await self.discount_service.load_data(discount_items)

        is_empty = await self.tax_service.is_empty()
        if is_empty:
            tax_file = Path(datadir) / 'taxes.csv'
            tax_items = await LoaderService.run_blocking_io(load_csv, tax_file)
            await self.tax_service.load_data(tax_items)

    @staticmethod
    async def run_blocking_io(func, *args) -> Any:
        """Run blocking I/O in executor."""
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, func, *args)
        return result


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f'{self.entity_name} not found, key: {entity_id}')


class TaxNotFoundError(Exception):
    entity_name: 'Tax'


class OrderNotFoundError(Exception):
    entity_name: 'Order'
