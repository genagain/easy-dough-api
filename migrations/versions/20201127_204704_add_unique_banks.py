"""add_unique_banks

Revision ID: eb83fb8d9d31
Revises: 1e33bd6fe8fc
Create Date: 2020-11-27 20:47:04.806647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb83fb8d9d31'
down_revision = '1e33bd6fe8fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('access_token', sa.String(length=255), nullable=False),
    sa.Column('logo', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index('unique_bank_index', 'banks', ['name', 'user_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('unique_bank_index', table_name='banks')
    op.drop_table('banks')
    # ### end Alembic commands ###
