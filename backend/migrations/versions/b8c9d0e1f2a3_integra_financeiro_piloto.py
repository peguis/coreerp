"""integra atendimento e repasse ao financeiro

Revision ID: b8c9d0e1f2a3
Revises: a7b8c9d0e1f2
Create Date: 2026-09-16

"""
from typing import Sequence, Union

from alembic import context, op
import sqlalchemy as sa


revision: str = "b8c9d0e1f2a3"
down_revision: Union[str, Sequence[str], None] = "a7b8c9d0e1f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if not context.is_offline_mode():
        fora_da_faixa = op.get_bind().execute(
            sa.text(
                "SELECT COUNT(*) FROM lancamentos_financeiros "
                "WHERE NOT (valor BETWEEN -9999999999.99 AND 9999999999.99)"
            )
        ).scalar_one()
        if fora_da_faixa:
            raise RuntimeError(
                "Existem valores financeiros fora da faixa Numeric(12,2). "
                "Corrija-os de forma auditavel antes desta migration."
            )

    op.alter_column(
        "lancamentos_financeiros",
        "valor",
        existing_type=sa.Float(),
        type_=sa.Numeric(precision=12, scale=2),
        existing_nullable=False,
        postgresql_using="round(valor::numeric, 2)",
    )
    op.add_column(
        "lancamentos_financeiros",
        sa.Column("origem_tipo", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "lancamentos_financeiros",
        sa.Column("origem_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "lancamentos_financeiros",
        sa.Column("forma_pagamento", sa.String(length=20), nullable=True),
    )
    op.create_check_constraint(
        "ck_lancamentos_financeiros_origem",
        "lancamentos_financeiros",
        "(origem_tipo IS NULL AND origem_id IS NULL) OR "
        "(origem_tipo IN ('ATENDIMENTO', 'REPASSE') AND origem_id IS NOT NULL)",
    )
    op.create_index(
        "uq_lancamentos_financeiros_origem_automatica",
        "lancamentos_financeiros",
        ["empresa_id", "origem_tipo", "origem_id"],
        unique=True,
        postgresql_where=sa.text(
            "origem_tipo IS NOT NULL AND origem_id IS NOT NULL"
        ),
    )

    op.add_column(
        "categorias_financeiras",
        sa.Column("chave_sistema", sa.String(length=50), nullable=True),
    )
    op.create_index(
        "uq_categorias_financeiras_chave_sistema",
        "categorias_financeiras",
        ["empresa_id", "chave_sistema"],
        unique=True,
        postgresql_where=sa.text("chave_sistema IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_categorias_financeiras_chave_sistema",
        table_name="categorias_financeiras",
    )
    op.drop_column("categorias_financeiras", "chave_sistema")

    op.drop_index(
        "uq_lancamentos_financeiros_origem_automatica",
        table_name="lancamentos_financeiros",
    )
    op.drop_constraint(
        "ck_lancamentos_financeiros_origem",
        "lancamentos_financeiros",
        type_="check",
    )
    op.drop_column("lancamentos_financeiros", "forma_pagamento")
    op.drop_column("lancamentos_financeiros", "origem_id")
    op.drop_column("lancamentos_financeiros", "origem_tipo")
    op.alter_column(
        "lancamentos_financeiros",
        "valor",
        existing_type=sa.Numeric(precision=12, scale=2),
        type_=sa.Float(),
        existing_nullable=False,
        postgresql_using="valor::double precision",
    )
