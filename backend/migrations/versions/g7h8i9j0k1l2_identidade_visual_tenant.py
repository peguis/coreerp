"""adiciona o codigo explicito da identidade visual do tenant

Revision ID: g7h8i9j0k1l2
Revises: f2a3b4c5d6e7
Create Date: 2026-09-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "g7h8i9j0k1l2"
down_revision: Union[str, Sequence[str], None] = "f2a3b4c5d6e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("empresas", sa.Column("identidade_codigo", sa.String(length=40), nullable=True))
    op.create_index("ix_empresas_identidade_codigo", "empresas", ["identidade_codigo"], unique=False)
    op.execute(
        sa.text(
            "UPDATE empresas SET identidade_codigo = 'hype' "
            "WHERE lower(nome) LIKE '%hype%' AND identidade_codigo IS NULL"
        )
    )
    op.execute(
        sa.text(
            "UPDATE empresas SET identidade_codigo = 'pegs-demo' "
            "WHERE identidade_codigo IS NULL AND ("
            "lower(nome) LIKE '%pegs%' OR lower(nome) LIKE '%coreerp%' OR "
            "lower(nome) LIKE '%demo%' OR lower(email) LIKE '%demo%'"
            ")"
        )
    )


def downgrade() -> None:
    op.drop_index("ix_empresas_identidade_codigo", table_name="empresas")
    op.drop_column("empresas", "identidade_codigo")
