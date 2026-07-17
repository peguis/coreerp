"""add empresa_id produtos

Revision ID: a48739bdb308
Revises: 7b57aaaa0b8e
Create Date: 2026-07-17 02:23:22.946168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a48739bdb308'
down_revision: Union[str, Sequence[str], None] = '7b57aaaa0b8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
