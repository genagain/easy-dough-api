"""add account to transactions

Revision ID: fb1f8028c476
Revises: 86ccb830a94f
Create Date: 2020-12-21 21:02:50.815116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb1f8028c476'
down_revision = '86ccb830a94f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('account_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'transactions', 'accounts', ['account_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'account_id')
    # ### end Alembic commands ###
