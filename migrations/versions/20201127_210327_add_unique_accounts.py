"""add_unique_accounts

Revision ID: 86ccb830a94f
Revises: eb83fb8d9d31
Create Date: 2020-11-27 21:03:27.529229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86ccb830a94f'
down_revision = 'eb83fb8d9d31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('plaid_account_id', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('type', sa.String(length=128), nullable=False),
    sa.Column('bank_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bank_id'], ['banks.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('plaid_account_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accounts')
    # ### end Alembic commands ###