"""adiciona modulo generico de servicos

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-09-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c3d4e5f6a7b8"
down_revision: Union[str, Sequence[str], None] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "servicos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column(
            "preco_padrao",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
            server_default=sa.text("0.00"),
        ),
        sa.Column(
            "ativo",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "length(trim(nome)) > 0",
            name="ck_servicos_nome_nao_vazio",
        ),
        sa.CheckConstraint(
            "preco_padrao >= 0",
            name="ck_servicos_preco_padrao_nao_negativo",
        ),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_servicos_empresa_id"),
        "servicos",
        ["empresa_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_servicos_empresa_id"), table_name="servicos")
    op.drop_table("servicos")
