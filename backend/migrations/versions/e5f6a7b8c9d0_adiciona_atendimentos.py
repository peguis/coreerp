"""adiciona atendimentos de servicos

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-09-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e5f6a7b8c9d0"
down_revision: Union[str, Sequence[str], None] = "d4e5f6a7b8c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "atendimentos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("profissional_id", sa.Integer(), nullable=False),
        sa.Column("servico_id", sa.Integer(), nullable=False),
        sa.Column("cliente_id", sa.Integer(), nullable=True),
        sa.Column("valor", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("forma_pagamento", sa.String(length=20), nullable=False),
        sa.Column("observacao", sa.Text(), nullable=True),
        sa.Column(
            "realizado_em",
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
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "valor > 0", name="ck_atendimentos_valor_positivo"
        ),
        sa.CheckConstraint(
            "forma_pagamento IN "
            "('PIX', 'DINHEIRO', 'CARTAO_DEBITO', 'CARTAO_CREDITO')",
            name="ck_atendimentos_forma_pagamento",
        ),
        sa.ForeignKeyConstraint(["cliente_id"], ["clientes.id"]),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["profissional_id"], ["profissionais.id"]),
        sa.ForeignKeyConstraint(["servico_id"], ["servicos.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for coluna in (
        "empresa_id",
        "profissional_id",
        "servico_id",
        "cliente_id",
        "forma_pagamento",
        "realizado_em",
    ):
        op.create_index(
            op.f(f"ix_atendimentos_{coluna}"),
            "atendimentos",
            [coluna],
            unique=False,
        )


def downgrade() -> None:
    for coluna in (
        "realizado_em",
        "forma_pagamento",
        "cliente_id",
        "servico_id",
        "profissional_id",
        "empresa_id",
    ):
        op.drop_index(
            op.f(f"ix_atendimentos_{coluna}"),
            table_name="atendimentos",
        )
    op.drop_table("atendimentos")
