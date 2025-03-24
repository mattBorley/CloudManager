"""Initial Migration

Revision ID: 428d265f4f2e
Revises:
Create Date: 2024-12-20 12:10:30.682523
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "428d265f4f2e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE users (
            id              INT AUTO_INCREMENT PRIMARY KEY,
            name            VARCHAR(255)        NOT NULL,
            email           VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255)        NOT NULL,
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS users")
