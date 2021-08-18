"""Added tables.

Revision ID: a794b80bcae4
Revises: 
Create Date: 2021-08-17 19:44:38.719317

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a794b80bcae4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('discounts',
    sa.Column('id', sa.Integer(), nullable=False, comment='Dicsount identifier.'),
    sa.Column('amount', sa.Numeric(precision=16, scale=2), nullable=False, comment='Amount for which this discount is applicable.'),
    sa.Column('rate', sa.Numeric(precision=16, scale=0), nullable=False, comment='Discount rate applied to amount measured in `%`.'),
    sa.PrimaryKeyConstraint('id'),
    comment='Table with discount rates applied to the amount.'
    )
    op.create_index(op.f('ix_discounts_amount'), 'discounts', ['amount'], unique=False)
    op.create_table('orders',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False, comment='Order identifier.'),
    sa.Column('ts', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Order timestamp.'),
    sa.Column('amount', sa.Numeric(precision=16, scale=2), nullable=False, comment='Amount of order received from calculator.'),
    sa.Column('after_discount', sa.Numeric(precision=16, scale=2), nullable=False, comment='Amount of order after discount has been applied.'),
    sa.Column('tax', sa.Numeric(precision=16, scale=2), nullable=False, comment='Tax sum calculated from discounted amount.'),
    sa.Column('total', sa.Numeric(precision=16, scale=2), nullable=False, comment='Total amount of order after discount and tax.'),
    sa.PrimaryKeyConstraint('id'),
    comment='Table with orders.'
    )
    op.create_index(op.f('ix_orders_ts'), 'orders', ['ts'], unique=False)
    op.create_table('taxes',
    sa.Column('id', sa.Integer(), nullable=False, comment='Tax identifier.'),
    sa.Column('state_name', sa.String(length=20), nullable=False, comment='Name of the state.'),
    sa.Column('rate', sa.Numeric(precision=16, scale=2), nullable=False, comment='Rate for the current state measured in `%`.'),
    sa.PrimaryKeyConstraint('id'),
    comment='Table with tax rates per state.'
    )
    op.create_index(op.f('ix_taxes_state_name'), 'taxes', ['state_name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_taxes_state_name'), table_name='taxes')
    op.drop_table('taxes')
    op.drop_index(op.f('ix_orders_ts'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_discounts_amount'), table_name='discounts')
    op.drop_table('discounts')
    # ### end Alembic commands ###