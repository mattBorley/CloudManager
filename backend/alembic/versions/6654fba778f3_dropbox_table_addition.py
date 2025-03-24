"""Dropbox Migration

Revision ID: 6654fba778f3
Revises: 428d265f4f2e
Create Date: 2025-02-28 12:10:30.682523
"""
from typing import Union, Sequence
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "6654fba778f3"
down_revision: str = "428d265f4f2e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'dropbox_accounts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('dropbox_user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('refresh_token', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True, server_default=sa.func.current_timestamp()),
        sa.Column('local_user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['local_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Drop dropbox_accounts table
    op.drop_table('dropbox_accounts')
