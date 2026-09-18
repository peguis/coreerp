"""configura recursos, categorias e snapshots da agenda

Revision ID: d9e0f1a2b3c4
Revises: c7d8e9f0a1b2
Create Date: 2026-09-18

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d9e0f1a2b3c4"
down_revision: Union[str, Sequence[str], None] = "c7d8e9f0a1b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "servicos",
        sa.Column("categoria", sa.String(length=50), nullable=True),
    )
    op.create_index("ix_servicos_categoria", "servicos", ["categoria"])
    op.create_check_constraint(
        "ck_servicos_categoria_nao_vazia",
        "servicos",
        "categoria IS NULL OR length(trim(categoria)) > 0",
    )
    op.alter_column(
        "servicos",
        "duracao_minutos",
        existing_type=sa.Integer(),
        server_default=sa.text("40"),
    )

    op.add_column(
        "recursos_agenda",
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=True,
            server_default=sa.text("'ATIVO'"),
        ),
    )
    op.execute(
        sa.text(
            "UPDATE recursos_agenda "
            "SET status = CASE WHEN ativo THEN 'ATIVO' ELSE 'INATIVO' END"
        )
    )
    op.alter_column(
        "recursos_agenda",
        "status",
        existing_type=sa.String(length=20),
        nullable=False,
    )
    op.create_index("ix_recursos_agenda_status", "recursos_agenda", ["status"])
    op.create_check_constraint(
        "ck_recursos_agenda_status",
        "recursos_agenda",
        "status IN ('ATIVO', 'INATIVO', 'MANUTENCAO')",
    )

    op.add_column(
        "agendamentos",
        sa.Column("duracao_minutos", sa.Integer(), nullable=True),
    )
    op.add_column(
        "agendamentos",
        sa.Column("preco_aplicado", sa.Numeric(12, 2), nullable=True),
    )

    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        op.execute(
            sa.text(
                "UPDATE agendamentos SET duracao_minutos = "
                "CAST((julianday(fim_em) - julianday(inicio_em)) * 1440 AS INTEGER)"
            )
        )
    else:
        op.execute(
            sa.text(
                "UPDATE agendamentos SET duracao_minutos = "
                "CAST(EXTRACT(EPOCH FROM (fim_em - inicio_em)) / 60 AS INTEGER)"
            )
        )
    op.execute(
        sa.text(
            "UPDATE agendamentos SET preco_aplicado = "
            "(SELECT s.preco_padrao FROM servicos AS s "
            "WHERE s.id = agendamentos.servico_id)"
        )
    )
    op.alter_column(
        "agendamentos",
        "duracao_minutos",
        existing_type=sa.Integer(),
        nullable=False,
    )
    op.alter_column(
        "agendamentos",
        "preco_aplicado",
        existing_type=sa.Numeric(12, 2),
        nullable=False,
    )
    op.create_check_constraint(
        "ck_agendamentos_duracao_valida",
        "agendamentos",
        "duracao_minutos > 0 AND duracao_minutos <= 1440",
    )
    op.create_check_constraint(
        "ck_agendamentos_preco_valido",
        "agendamentos",
        "preco_aplicado >= 0",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_agendamentos_preco_valido", "agendamentos", type_="check"
    )
    op.drop_constraint(
        "ck_agendamentos_duracao_valida", "agendamentos", type_="check"
    )
    op.drop_column("agendamentos", "preco_aplicado")
    op.drop_column("agendamentos", "duracao_minutos")

    op.drop_constraint(
        "ck_recursos_agenda_status", "recursos_agenda", type_="check"
    )
    op.drop_index("ix_recursos_agenda_status", table_name="recursos_agenda")
    op.drop_column("recursos_agenda", "status")

    op.drop_constraint(
        "ck_servicos_categoria_nao_vazia", "servicos", type_="check"
    )
    op.drop_index("ix_servicos_categoria", table_name="servicos")
    op.drop_column("servicos", "categoria")
    op.alter_column(
        "servicos",
        "duracao_minutos",
        existing_type=sa.Integer(),
        server_default=sa.text("60"),
    )
