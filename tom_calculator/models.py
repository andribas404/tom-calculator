from sqlalchemy import Column, Integer, String, Numeric
from tom_calculator.database import BaseModel


class Tax(BaseModel):
    __tablename__ = 'taxes'
    id = Column(Integer, primary_key=True)
    state_name = Column(String(20))
    rate = Column(Numeric(14, 2))


class Discount(BaseModel):
    __tablename__ = 'discounts'
    id = Column(Integer, primary_key=True)
    range_start = Column(Numeric(14, 2))
    range_end = Column(Numeric(14, 2))
    rate = Column(Numeric(14, 2))
