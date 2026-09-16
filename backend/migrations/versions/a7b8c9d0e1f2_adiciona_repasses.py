"""adiciona repasses e seus itens auditaveis

Revision ID: a7b8c9d0e1f2
Revises: f6a7b8c9d0e1
Create Date: 2026-09-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a7b8c9d0e1f2"
down_revision: Union[str, Sequence[str], None] = "f6a7b8c9d0e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "repasses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("profissional_id", sa.Integer(), nullable=False),
        sa.Column("created_by_usuario_id", sa.Integer(), nullable=False),
        sa.Column("valor", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("forma_pagamento", sa.String(length=20), nullable=False),
        sa.Column("observacao", sa.Text(), nullable=True),
        sa.Column(
            "pago_em",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint("valor > 0", name="ck_repasses_valor_positivo"),
        sa.CheckConstraint(
            "forma_pagamento IN ('PIX', 'DINHEIRO', 'TRANSFERENCIA')",
            name="ck_repasses_forma_pagamento",
        ),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["profissional_id"], ["profissionais.id"]),
        sa.ForeignKeyConstraint(["created_by_usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for coluna in (
        "empresa_id",
        "profissional_id",
        "created_by_usuario_id",
        "pago_em",
    ):
        op.create_index(
            op.f(f"ix_repasses_{coluna}"),
            "repasses",
            [coluna],
            unique=False,
        )

    op.create_table(
        "repasse_itens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("repasse_id", sa.Integer(), nullable=False),
        sa.Column("atendimento_id", sa.Integer(), nullable=False),
        sa.Column("valor", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "valor > 0", name="ck_repasse_itens_valor_positivo"
        ),
        sa.ForeignKeyConstraint(["atendimento_id"], ["atendimentos.id"]),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["repasse_id"], ["repasses.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "repasse_id",
            "atendimento_id",
            name="uq_repasse_itens_repasse_atendimento",
        ),
    )
    for coluna in ("empresa_id", "repasse_id", "atendimento_id"):
        op.create_index(
            op.f(f"ix_repasse_itens_{coluna}"),
            "repasse_itens",
            [coluna],
            unique=False,
        )


def downgrade() -> None:
    for coluna in ("atendimento_id", "repasse_id", "empresa_id"):
        op.drop_index(
            op.f(f"ix_repasse_itens_{coluna}"),
            table_name="repasse_itens",
        )
    op.drop_table("repasse_itens")

    for coluna in (
        "pago_em",
        "created_by_usuario_id",
        "profissional_id",
        "empresa_id",
    ):
        op.drop_index(
            op.f(f"ix_repasses_{coluna}"),
            table_name="repasses",
        )
    op.drop_table("repasses")
