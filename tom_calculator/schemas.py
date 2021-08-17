import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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


class CalculatorIn(BaseModel):
    """Calculator input."""
    items: List[CalculatorItemIn]
