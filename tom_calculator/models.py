"""Models."""
import logging
from typing import Type

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from tom_calculator.database import Base

logger = logging.getLogger(__name__)

TBase = Type[Base]


class Tax(Base):
    """Tax model."""
    __tablename__ = 'taxes'
    __table_args__ = {'comment': 'Table with tax rates per state.'}

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        doc='Tax identifier.',
        comment='Tax identifier.',
    )
    state_name = sa.Column(
        sa.String(20),
        nullable=False,
        index=True,
        unique=True,
        doc='Name of the state.',
        comment='Name of the state.',
    )
    rate = sa.Column(
        sa.Numeric(16, 2),
        nullable=False,
        doc='Rate for the current state measured in `%`.',
        comment='Rate for the current state measured in `%`.',
    )


class Discount(Base):
    """Discount model."""
    __tablename__ = 'discounts'
    __table_args__ = {'comment': 'Table with discount rates applied to the amount.'}

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        doc='Dicsount identifier.',
        comment='Dicsount identifier.',
    )
    amount = sa.Column(
        sa.Numeric(16, 2),
        nullable=False,
        index=True,
        doc='Amount for which this discount is applicable.',
        comment='Amount for which this discount is applicable.',
    )
    rate = sa.Column(
        sa.Numeric(16, 0),
        nullable=False,
        doc='Discount rate applied to amount measured in `%`.',
        comment='Discount rate applied to amount measured in `%`.',
    )


class Order(Base):
    """Order model."""
    __tablename__ = 'orders'
    __table_args__ = {'comment': 'Table with orders.'}
    __mapper_args__ = {'eager_defaults': True}

    id = sa.Column(  # type: ignore[misc]
        UUID,
        primary_key=True,
        server_default=sa.func.uuid_generate_v4(),
        doc='Order identifier.',
        comment='Order identifier.',
    )
    ts = sa.Column(  # type: ignore[misc]
        sa.DateTime,
        server_default=sa.func.now(),
        nullable=False,
        index=True,
        doc='Order timestamp.',
        comment='Order timestamp.',
    )
    amount = sa.Column(
        sa.Numeric(16, 2),
        nullable=False,
        doc='Amount of order received from calculator.',
        comment='Amount of order received from calculator.',
    )
    # after_discount = amount - discount
    after_discount = sa.Column(
        sa.Numeric(16, 2),
        nullable=False,
        doc='Amount of order after discount has been applied.',
        comment='Amount of order after discount has been applied.',
    )
    # tax = after_discount * rate
    tax = sa.Column(
        sa.Numeric(16, 2),
        nullable=False,
        doc='Tax sum calculated from discounted amount.',
        comment='Tax sum calculated from discounted amount.',
    )
    # total = after_discount + tax
    total = sa.Column(
        sa.Numeric(16, 2),
        nullable=False,
        doc='Total amount of order after discount and tax.',
        comment='Total amount of order after discount and tax.',
    )
