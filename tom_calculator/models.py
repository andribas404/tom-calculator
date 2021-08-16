import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import MONEY, UUID
from tom_calculator.database import BaseModel


class Tax(BaseModel):
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
        sa.Numeric(16, 4),
        nullable=False,
        doc='Rate for the current state measured in `%`.',
        comment='Rate for the current state measured in `%`.',
    )


class Discount(BaseModel):
    __tablename__ = 'discounts'
    __table_args__ = {'comment': 'Table with discount rates applied to amount in range.'}

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        doc='Dicsount identifier.',
        comment='Dicsount identifier.',
    )
    range_start = sa.Column(
        MONEY,
        nullable=False,
        doc='Start of range inclusive, so amount should be in [start, end).',
        comment='Start of range inclusive, so amount should be in [start, end).',
    )
    range_end = sa.Column(
        MONEY,
        nullable=False,
        doc='End of range exclusive, so amount should be in [start, end).',
        comment='End of range exclusive, so amount should be in [start, end).',
    )
    rate = sa.Column(
        sa.Numeric(16, 4),
        nullable=False,
        doc='Discount rate applied to amount in that range measured in `%`.',
        comment='Discount rate applied to amount in that range measured in `%`.',
    )


class Order(BaseModel):
    __tablename__ = 'orders'
    __table_args__ = {'comment': 'Table with orders.'}

    id = sa.Column(
        UUID,
        primary_key=True,
        server_default=sa.func.uuid_generate_v4(),
        doc='Order identifier.',
        comment='Order identifier.',
    )
    ts = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        nullable=False,
        doc='Order timestamp.',
        comment='Order timestamp.',
    )
    amount = sa.Column(
        MONEY,
        nullable=False,
        doc='Amount of order received from calculator.',
        comment='Amount of order received from calculator.',
    )
    after_discount = sa.Column(
        MONEY,
        nullable=False,
        doc='Amount of order after discount has been applied.',
        comment='Amount of order after discount has been applied.',
    )
    tax = sa.Column(
        MONEY,
        nullable=False,
        doc='Tax sum calculated from discounted amount.',
        comment='Tax sum calculated from discounted amount.',
    )
    total = sa.Column(
        MONEY,
        nullable=False,
        doc='Total amount of order after discount and tax.',
        comment='Total amount of order after discount and tax.',
    )
