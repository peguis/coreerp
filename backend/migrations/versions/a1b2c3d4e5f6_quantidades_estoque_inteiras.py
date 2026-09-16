"""alinha quantidades de estoque para inteiros

Revision ID: a1b2c3d4e5f6
Revises: 1642469f38b1
Create Date: 2026-09-15

"""
from typing import Sequence, Union

from alembic import context, op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "1642469f38b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _ensure_no_fractional_stock() -> None:
    if context.is_offline_mode():
        return

    connection = op.get_bind()

    has_fractional_stock = connection.execute(
        sa.text(
            """
            SELECT EXISTS (
                SELECT 1
                FROM produtos
                WHERE estoque <> TRUNC(estoque)
                   OR estoque_minimo <> TRUNC(estoque_minimo)
                   OR estoque_maximo <> TRUNC(estoque_maximo)
            )
            """
        )
    ).scalar()

    if has_fractional_stock:
        raise RuntimeError(
            "Existem quantidades fracionárias em produtos; "
            "a migração foi interrompida para evitar truncamento."
        )


def upgrade() -> None:
    """Upgrade schema."""
    _ensure_no_fractional_stock()

    op.alter_column(
        "produtos",
        "estoque",
        existing_type=sa.Float(),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="estoque::integer"
    )
    op.alter_column(
        "produtos",
        "estoque_minimo",
        existing_type=sa.Float(),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="estoque_minimo::integer"
    )
    op.alter_column(
        "produtos",
        "estoque_maximo",
        existing_type=sa.Float(),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="estoque_maximo::integer"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "produtos",
        "estoque_maximo",
        existing_type=sa.Integer(),
        type_=sa.Float(),
        existing_nullable=False,
        postgresql_using="estoque_maximo::double precision"
    )
    op.alter_column(
        "produtos",
        "estoque_minimo",
        existing_type=sa.Integer(),
        type_=sa.Float(),
        existing_nullable=False,
        postgresql_using="estoque_minimo::double precision"
    )
    op.alter_column(
        "produtos",
        "estoque",
        existing_type=sa.Integer(),
        type_=sa.Float(),
        existing_nullable=False,
        postgresql_using="estoque::double precision"
    )
