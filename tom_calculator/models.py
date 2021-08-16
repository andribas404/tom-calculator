import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import MONEY, UUID
from tom_calculator.database import BaseModel


class Tax(BaseModel):
    __tablename__ = 'taxes'

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        doc='',
        comment='',
    )
    state_name = sa.Column(
        sa.String(20),
        nullable=False,
        doc='',
        comment='',
    )
    rate = sa.Column(
        sa.Numeric(16, 4),
        nullable=False,
        doc='',
        comment='',
    )


class Discount(BaseModel):
    __tablename__ = 'discounts'

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        doc='',
        comment='',
    )
    range_start = sa.Column(
        MONEY,
        nullable=False,
        doc='',
        comment='',
    )
    range_end = sa.Column(
        MONEY,
        nullable=False,
        doc='',
        comment='',
    )
    rate = sa.Column(
        sa.Numeric(16, 4),
        nullable=False,
        doc='',
        comment='',
    )


class Order(BaseModel):
    id = sa.Column(
        UUID,
        primary_key=True,
        server_default=sa.func.uuid_generate_v4(),
        doc='',
        comment='',
    )
    ts = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        nullable=False,
        doc='',
        comment='',
    )
    amount = sa.Column(
        MONEY,
        nullable=False,
        doc='',
        comment='',
    )
    after_discount = sa.Column(
        MONEY,
        nullable=False,
        doc='',
        comment='',
    )
    tax = sa.Column(
        MONEY,
        nullable=False,
        doc='',
        comment='',
    )
    total = sa.Column(
        MONEY,
        nullable=False,
        doc='',
        comment='',
    )
