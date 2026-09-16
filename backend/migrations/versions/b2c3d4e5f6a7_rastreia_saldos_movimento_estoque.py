"""adiciona saldos anterior e posterior aos movimentos de estoque

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-09-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "movimentos_estoque",
        sa.Column("estoque_anterior", sa.Integer(), nullable=True)
    )
    op.add_column(
        "movimentos_estoque",
        sa.Column("estoque_posterior", sa.Integer(), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("movimentos_estoque", "estoque_posterior")
    op.drop_column("movimentos_estoque", "estoque_anterior")
