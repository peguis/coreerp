"""identifica pedidos externos do e-commerce

Revision ID: k1l2m3n4o5p6
Revises: j0k1l2m3n4o5
Create Date: 2026-10-04
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "k1l2m3n4o5p6"
down_revision: Union[str, Sequence[str], None] = "j0k1l2m3n4o5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "vendas",
        sa.Column(
            "origem",
            sa.String(length=30),
            nullable=False,
            server_default="ERP"
        )
    )
    op.add_column(
        "vendas",
        sa.Column("pedido_externo_id", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "vendas",
        sa.Column("chave_idempotencia", sa.String(length=80), nullable=True)
    )
    op.add_column(
        "vendas",
        sa.Column("observacoes", sa.Text(), nullable=True)
    )
    op.add_column(
        "vendas",
        sa.Column("endereco_entrega", sa.Text(), nullable=True)
    )
    op.create_index(
        "ix_vendas_pedido_externo_id",
        "vendas",
        ["pedido_externo_id"],
        unique=False
    )
    op.create_index(
        "ix_vendas_chave_idempotencia",
        "vendas",
        ["chave_idempotencia"],
        unique=False
    )
    op.create_index(
        "uq_vendas_empresa_chave_idempotencia",
        "vendas",
        ["empresa_id", "chave_idempotencia"],
        unique=True
    )


def downgrade() -> None:
    op.drop_index(
        "uq_vendas_empresa_chave_idempotencia",
        table_name="vendas"
    )
    op.drop_index("ix_vendas_chave_idempotencia", table_name="vendas")
    op.drop_index("ix_vendas_pedido_externo_id", table_name="vendas")
    op.drop_column("vendas", "endereco_entrega")
    op.drop_column("vendas", "observacoes")
    op.drop_column("vendas", "chave_idempotencia")
    op.drop_column("vendas", "pedido_externo_id")
    op.drop_column("vendas", "origem")
