"""Test /order endpoint."""
import pytest
from syrupy.filters import paths

from tom_calculator.models import Discount, Tax


class TestOrderPost:
    """Test order creation."""

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
        {"items": [{"quantity": 0, "price": 0}], "state_name": "state"},
        {"items": [{"quantity": 0, "price": 20}], "state_name": "state"},
        {"items": [{"quantity": 100, "price": 12.34}], "state_name": "state"},
        {"items": [{"quantity": 7, "price": 0.99}], "state_name": "state"},
    ])
    def test_valid(self, client, snapshot, payload):
        """Test valid order creation."""
        response = client.post('/order', json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data == snapshot(exclude=paths("id", "ts"))

    @pytest.mark.parametrize(('payload', 'status_code'), [
        ({"items2": [{"quantity1": 0, "price3": 0}], "state_name4": "state"}, 422),
        ({"key": "value"}, 422),
        ({"items": [{"quantity": 0}], "state_name": "state"}, 422),
        ({"items": [{"quantity": 0, "price": 0}, {"quantity2": 0, "price3": 0}], "state_name": "state"}, 422),
        ({"items": [{"quantity": 0, "price": 0}], }, 422),
    ])
    def test_incorrect_schema(self, client, snapshot, payload, status_code):
        """Incorrect schema."""
        response = client.post('/order', json=payload)
        assert response.status_code == status_code
        data = response.json()
        assert data == snapshot

    @pytest.mark.parametrize(('payload', 'status_code'), [
        ({"items": [], "state_name": "state"}, 422),
    ])
    def test_empty_list(self, client, snapshot, payload, status_code):
        """Empty list."""
        response = client.post('/order', json=payload)
        assert response.status_code == status_code
        data = response.json()
        assert data == snapshot

    @pytest.mark.parametrize(('payload', 'status_code'), [
        ({"items": [{"quantity": "abc", "price": 0}], "state_name": "state"}, 422),
        ({"items": [{"quantity": None, "price": 0}], "state_name": "state"}, 422),
    ])
    def test_quantity_not_int(self, client, snapshot, payload, status_code):
        """Quantity not int."""
        response = client.post('/order', json=payload)
        assert response.status_code == status_code
        data = response.json()
        assert data == snapshot

    @pytest.mark.parametrize(('payload', 'status_code'), [
        ({"items": [{"quantity": -5, "price": 0}], "state_name": "state"}, 422),
    ])
    def test_negative_quantity(self, client, snapshot, payload, status_code):
        """Negative quantity."""
        response = client.post('/order', json=payload)
        assert response.status_code == status_code
        data = response.json()
        assert data == snapshot

    @pytest.mark.parametrize(('payload', 'status_code'), [
        ({"items": [{"quantity": 0, "price": "abc"}], "state_name": "state"}, 422),
        ({"items": [{"quantity": 0, "price": None}], "state_name": "state"}, 422),
    ])
    def test_price_not_float(self, client, snapshot, payload, status_code):
        """Price not float."""
        response = client.post('/order', json=payload)
        assert response.status_code == status_code
        data = response.json()
        assert data == snapshot

    @pytest.mark.parametrize(('payload', 'status_code'), [
        ({"items": [{"quantity": 0, "price": -10}], "state_name": "state"}, 422),
    ])
    def test_negative_price(self, client, snapshot, payload, status_code):
        """Negative price."""
        response = client.post('/order', json=payload)
        assert response.status_code == status_code
        data = response.json()
        assert data == snapshot

    @pytest.mark.parametrize(('payload', 'status_code'), [
        ({"items": [{"quantity": 0, "price": 0.235}], "state_name": "state"}, 422),
        ({"items": [{"quantity": 0, "price": 23423.1412}], "state_name": "state"}, 422),
        ({"items": [{"quantity": 0, "price": 23423.141}], "state_name": "state"}, 422),
        ({"items": [{"quantity": 0, "price": 23423.149}], "state_name": "state"}, 422),
        ({"items": [{"quantity": 0, "price": 23423.145}], "state_name": "state"}, 422),
        ({"items": [{"quantity": 0, "price": 23423.149999}], "state_name": "state"}, 422),
    ])
    def test_price_not_money(self, client, snapshot, payload, status_code):
        """Price not money."""
        response = client.post('/order', json=payload)
        assert response.status_code == status_code
        data = response.json()
        assert data == snapshot

    @pytest.mark.parametrize(('payload', 'status_code'), [
        ({"items": [{"quantity": 0, "price": 0}], "state_name": "state1"}, 400),
        ({"items": [{"quantity": 0, "price": 0}], "state_name": "st"}, 400),
    ])
    def test_state_not_exists(self, client, snapshot, payload, status_code):
        """State not exists."""
        response = client.post('/order', json=payload)
        assert response.status_code == status_code
        data = response.json()
        assert data == snapshot

    @pytest.mark.parametrize(('payload', 'status_code'), [
        ({"items": [{"quantity": 0, "price": 0.230}], "state_name": "state"}, 201),
        ({"items": [{"quantity": 0, "price": "340.5600"}], "state_name": "state"}, 201),
    ])
    def test_price_correct(self, client, snapshot, payload, status_code):
        """Price correct."""
        response = client.post('/order', json=payload)
        assert response.status_code == status_code
        data = response.json()
        assert data == snapshot(exclude=paths("id", "ts"))

    @pytest.mark.parametrize(('payload', 'status_code'), [
        ({"items": [{"quantity": 10, "price": 10}], "state_name": "state"}, 201),
        ({"items": [{"quantity": 10, "price": 100}], "state_name": "state"}, 201),
    ])
    def test_amount_equal_to_discount(self, client, snapshot, payload, status_code):
        """Amount equal to discount."""
        response = client.post('/order', json=payload)
        assert response.status_code == status_code
        data = response.json()
        assert data == snapshot(exclude=paths("id", "ts"))

    @pytest.mark.parametrize(('payload', 'status_code'), [
        ({"items": [{"quantity": 10, "price": 9.99}], "state_name": "state"}, 201),
    ])
    def test_amount_less_than_discount(self, client, snapshot, payload, status_code):
        """Amount less than discount."""
        response = client.post('/order', json=payload)
        assert response.status_code == status_code
        data = response.json()
        assert data == snapshot(exclude=paths("id", "ts"))

    @pytest.mark.parametrize(('payload', 'status_code'), [
        ({"items": [{"quantity": 10, "price": 10}, {"quantity": 1, "price": 0.01}], "state_name": "state"}, 201),
    ])
    def test_amount_greater_than_discount(self, client, snapshot, payload, status_code):
        """Amount greater than discount."""
        response = client.post('/order', json=payload)
        assert response.status_code == status_code
        data = response.json()
        assert data == snapshot(exclude=paths("id", "ts"))

    @pytest.mark.parametrize(('payload', 'status_code'), [
        ({"items": [{"quantity": 10, "price": 300}], "state_name": "state"}, 201),
    ])
    def test_best_discount_applied(self, client, snapshot, payload, status_code):
        """Best discount applied."""
        response = client.post('/order', json=payload)
        assert response.status_code == status_code
        data = response.json()
        assert data == snapshot(exclude=paths("id", "ts"))
