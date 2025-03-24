"""Revision on dropbox_accounts

Revision ID: b582c534bab1
Revises: 6654fba778f3
Create Date: 2025-03-04 06:35:45.747831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b582c534bab1'
down_revision: Union[str, None] = '6654fba778f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'dropbox_accounts',
        'dropbox_user_id',
        type_=sa.String(length=255),
        existing_type=sa.Integer(),
    )

def downgrade():
    op.alter_column(
        'dropbox_accounts',
        'dropbox_user_id',
        type_=sa.Integer(),  # new type
        existing_type=sa.String(length=255),
    )
