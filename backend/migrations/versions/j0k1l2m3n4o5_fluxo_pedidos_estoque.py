"""controla baixa de estoque no fluxo de pedidos

Revision ID: j0k1l2m3n4o5
Revises: i9j0k1l2m3n4
Create Date: 2026-10-04
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "j0k1l2m3n4o5"
down_revision: Union[str, Sequence[str], None] = "i9j0k1l2m3n4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # As vendas existentes já baixavam estoque ao serem criadas. O valor
    # inicial true preserva esse comportamento; novos pedidos PENDENTE
    # sobrescrevem o campo para false no serviço.
    op.add_column(
        "vendas",
        sa.Column(
            "estoque_baixado",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true")
        )
    )


def downgrade() -> None:
    op.drop_column("vendas", "estoque_baixado")
