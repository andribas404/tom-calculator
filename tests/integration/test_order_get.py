"""Test /order/{item_id} endpoint."""
import datetime
import decimal
import uuid
import pytest
from sqlalchemy.future import select

from tom_calculator.models import Discount, Order, Tax


@pytest.mark.asyncio
class TestOrderGet:
    """Test order get."""
    @pytest.fixture(autouse=True)
    async def _setup(self, app):
        """Setup entities."""
        async with app.container.db().session() as session:
            tax = Tax(state_name='state', rate=5)
            discount = Discount(amount=100, rate=3)
            discount = Discount(amount=1000, rate=30)
            session.add(tax)
            session.add(discount)

    @pytest.mark.parametrize('payload', [
        {"items": [{"quantity": 100, "price": 12.34}], "state_name": "state"},
    ])
    async def test_valid(self, app, async_client, payload):
        """Test valid order get."""
        response = await async_client.post('/order', json=payload)
        assert response.status_code == 201
        data = response.json()
        assert 'id' in data
        item_id = data['id']
        response_order = await async_client.get(f'/order/{item_id}')
        assert response_order.status_code == 200
        item_api = response_order.json()
        assert data == item_api

        stmt = (
            select(
                Order,
            )
            .filter(Order.id == item_id)
        )
        async with app.container.db().session() as session:
            res = await session.execute(stmt)
        item_db = res.scalar()
        assert item_db is not None
        for key, value in data.items():
            value_db = getattr(item_db, key)
            if isinstance(value_db, datetime.datetime):
                value_db = value_db.isoformat()
            if isinstance(value_db, uuid.UUID):
                value_db = str(value_db)
            if isinstance(value_db, decimal.Decimal):
                value = decimal.Decimal(str(value))
            assert value_db == value
