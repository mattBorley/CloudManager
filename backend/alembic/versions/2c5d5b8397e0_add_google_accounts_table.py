"""Add google_accounts table

Revision ID: 2c5d5b8397e0
Revises: b582c534bab1
Create Date: 2025-03-18 04:27:54.532179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c5d5b8397e0'
down_revision: Union[str, None] = 'b582c534bab1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'google_accounts',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('refresh_token', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True, server_default=sa.func.current_timestamp()),
        sa.Column('local_user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['local_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('google_accounts')

