"""adiciona perfil usuario

Revision ID: b2ed187650e4
Revises: ddaa411bb5e0
Create Date: 2026-07-21 21:34:18.800713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2ed187650e4'
down_revision: Union[str, Sequence[str], None] = 'ddaa411bb5e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'usuarios',
        sa.Column(
            'perfil',
            sa.String(),
            nullable=False,
            server_default='usuario'
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('usuarios', 'perfil')
