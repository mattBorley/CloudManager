"""Add box_accounts table

Revision ID: 9c82e4f664dc
Revises: 2c5d5b8397e0
Create Date: 2025-03-23 13:38:20.760658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c82e4f664dc'
down_revision: Union[str, None] = '2c5d5b8397e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'box_accounts',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('refresh_token', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True, server_default=sa.func.current_timestamp()),
        sa.Column('local_user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['local_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('box_accounts')