"""Test /order endpoint."""
import pytest

from tom_calculator.models import Discount, Tax


class TestOrderPost:
    """Test order creation."""

    @pytest.fixture(autouse=True)
    async def _setup(self, app):
        """Setup entities."""
        async with app.container.db().session() as session:
            tax = Tax(state_name='state', rate=5)
            discount = Discount(amount=100, rate=3)
            session.add(tax)
            session.add(discount)

    @pytest.mark.parametrize(('payload', 'expected'), [
        (
            {"items": [{"quantity": 0, "price": 0}], "state_name": "state"},
            {
                "amount": 0,
                "after_discount": 0,
                "tax": 0,
                "total": 0,
            }
        ),
        (
            {"items": [{"quantity": 0, "price": 0}], "state_name": "state"},
            {
                "amount": 0,
                "after_discount": 0,
                "tax": 0,
                "total": 0,
            }
        ),
        (
            {"items": [{"quantity": 100, "price": 12.34}], "state_name": "state"},
            {
                "amount": 1234.0,
                "after_discount": 1196.98,
                "tax": 59.85,
                "total": 1137.13,
            }
        ),
        (
            {"items": [{"quantity": 7, "price": 0.99}], "state_name": "state"},
            {
                "amount": 6.93,
                "after_discount": 6.93,
                "tax": 0.35,
                "total": 6.58,
            }
        ),
    ])
    def test_valid(self, client, payload, expected):
        """Test valid order creation."""
        response = client.post('/order', json=payload)
        assert response.status_code == 201
        data = response.json()
        data.pop('id')
        data.pop('ts')
        assert data == expected
