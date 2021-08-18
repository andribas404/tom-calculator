"""Schemas."""
import datetime
import logging
from decimal import Decimal
from numbers import Real
from typing import List, Sequence
from uuid import UUID

from pydantic import BaseModel, validator

from tom_calculator.util import round_down

logger = logging.getLogger(__name__)


def validate_money_format(value: Decimal) -> Decimal:
    """Validate that value is in XXX[.CC] format.

    Checks that value contains no more than 2 digits in fraction.
    """
    assert round_down(value) == value, 'Not the money format.'
    return value


def validate_not_empty(value: Sequence) -> Sequence:
    """Validate that sequence is not empty."""
    assert len(value), 'Empty sequence is not allowed.'
    return value


def validate_not_negative(value: Real) -> Real:
    """Validate that value is not negative."""
    assert value >= 0, 'Negative number is not allowed.'
    return value


class TaxItem(BaseModel):
    """Tax Item."""
    state_name: str
    rate: Decimal


class TaxItemIn(TaxItem):
    """Tax Item input."""
    pass


class TaxItemOut(TaxItem):
    """Tax Item output."""
    id: int


class DiscountItem(BaseModel):
    """Discount Item."""
    amount: Decimal
    rate: int


class DiscountItemIn(DiscountItem):
    """Discount Item input."""


class DiscountItemOut(DiscountItem):
    """Discount Item output."""
    id: int


class OrderItemOut(BaseModel):
    """Order Item output."""
    id: UUID
    ts: datetime.datetime
    amount: Decimal
    after_discount: Decimal
    tax: Decimal
    total: Decimal


class CalculatorItemIn(BaseModel):
    """Calculator Item input."""
    quantity: int
    price: Decimal

    # validators
    _validate_not_negative = validator('quantity', 'price', allow_reuse=True)(validate_not_negative)
    _validate_money = validator('price', allow_reuse=True)(validate_money_format)


class CalculatorIn(BaseModel):
    """Calculator input."""
    items: List[CalculatorItemIn]
    state_name: str

    # validators
    _validate_not_empty = validator('items', allow_reuse=True)(validate_not_empty)
