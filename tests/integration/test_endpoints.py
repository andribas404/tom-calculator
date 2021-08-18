import pytest

from tom_calculator.models import Tax

class TestAPIOrder:
    @pytest.fixture(autouse=True)
    async def _setup(self, app):
        """Setup entities.

        See https://github.com/FactoryBoy/factory_boy/pull/803
        """
        async with app.container.db().session() as session:
            tax = Tax(state_name='state', rate=5)
            session.add(tax)
            await session.commit()

    @pytest.mark.parametrize(('payload', 'expected'), [
        (
            {"items": [{"quantity": 0, "price": 0}], "state_name": "state"},
            {
                "amount": 0,
                "after_discount": 0,
                "tax": 0,
                "total": 0
            }
        ),
        (
            {"items": [{"quantity": 0, "price": 0}], "state_name": "state"},
            {
                "amount": 0,
                "after_discount": 0,
                "tax": 0,
                "total": 0
            }
        ),
    ])
    def test_valid(self, client, payload, expected):
        response = client.post('/order', json=payload)
        assert response.status_code == 201
        data = response.json()
        data.pop('id')
        data.pop('ts')
        assert data == expected
