"""renamed expenses to bill

Revision ID: abfb62d1e907
Revises: 34c035e37e0c
Create Date: 2025-06-30 12:34:19.686065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abfb62d1e907'
down_revision: Union[str, Sequence[str], None] = '34c035e37e0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
