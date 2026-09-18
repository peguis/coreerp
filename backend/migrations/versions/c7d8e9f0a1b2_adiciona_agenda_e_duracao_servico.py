"""adiciona agenda, recursos e duracao dos servicos

Revision ID: c7d8e9f0a1b2
Revises: b8c9d0e1f2a3
Create Date: 2026-09-17

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c7d8e9f0a1b2"
down_revision: Union[str, Sequence[str], None] = "b8c9d0e1f2a3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "servicos",
        sa.Column(
            "duracao_minutos",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("60"),
        ),
    )
    op.add_column(
        "servicos",
        sa.Column(
            "requer_recurso",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "servicos",
        sa.Column("tipo_recurso", sa.String(length=30), nullable=True),
    )
    op.add_column(
        "servicos",
        sa.Column(
            "modo_selecao_recurso",
            sa.String(length=20),
            nullable=True,
            server_default=sa.text("'AUTOMATICO'"),
        ),
    )
    op.create_check_constraint(
        "ck_servicos_duracao_valida",
        "servicos",
        "duracao_minutos > 0 AND duracao_minutos <= 1440",
    )

    op.create_table(
        "recursos_agenda",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("tipo", sa.String(length=30), nullable=False),
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
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "empresa_id", "nome", name="uq_recursos_agenda_empresa_nome"
        ),
        sa.CheckConstraint(
            "length(trim(nome)) > 0",
            name="ck_recursos_agenda_nome_nao_vazio",
        ),
        sa.CheckConstraint(
            "length(trim(tipo)) > 0",
            name="ck_recursos_agenda_tipo_nao_vazio",
        ),
    )
    op.create_index(
        "ix_recursos_agenda_empresa_id",
        "recursos_agenda",
        ["empresa_id"],
    )
    op.create_index(
        "ix_recursos_agenda_tipo",
        "recursos_agenda",
        ["tipo"],
    )

    op.create_table(
        "agendamentos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("profissional_id", sa.Integer(), nullable=False),
        sa.Column("servico_id", sa.Integer(), nullable=False),
        sa.Column("cliente_id", sa.Integer(), nullable=True),
        sa.Column("cliente_avulso_nome", sa.String(length=150), nullable=True),
        sa.Column("recurso_id", sa.Integer(), nullable=True),
        sa.Column("criado_por_usuario_id", sa.Integer(), nullable=False),
        sa.Column("inicio_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fim_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default=sa.text("'AGENDADO'"),
        ),
        sa.Column("observacao", sa.Text(), nullable=True),
        sa.Column("motivo_cancelamento", sa.Text(), nullable=True),
        sa.Column("cancelado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelado_por_usuario_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["profissional_id"], ["profissionais.id"]),
        sa.ForeignKeyConstraint(["servico_id"], ["servicos.id"]),
        sa.ForeignKeyConstraint(["cliente_id"], ["clientes.id"]),
        sa.ForeignKeyConstraint(["recurso_id"], ["recursos_agenda.id"]),
        sa.ForeignKeyConstraint(["criado_por_usuario_id"], ["usuarios.id"]),
        sa.ForeignKeyConstraint(
            ["cancelado_por_usuario_id"], ["usuarios.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "fim_em > inicio_em",
            name="ck_agendamentos_fim_depois_inicio",
        ),
        sa.CheckConstraint(
            "status IN ('AGENDADO', 'CONFIRMADO', 'CONCLUIDO', 'CANCELADO', 'NAO_COMPARECEU')",
            name="ck_agendamentos_status",
        ),
    )
    for nome, coluna in (
        ("ix_agendamentos_empresa_id", "empresa_id"),
        ("ix_agendamentos_profissional_id", "profissional_id"),
        ("ix_agendamentos_servico_id", "servico_id"),
        ("ix_agendamentos_cliente_id", "cliente_id"),
        ("ix_agendamentos_recurso_id", "recurso_id"),
        ("ix_agendamentos_criado_por_usuario_id", "criado_por_usuario_id"),
        ("ix_agendamentos_inicio_em", "inicio_em"),
        ("ix_agendamentos_fim_em", "fim_em"),
        ("ix_agendamentos_status", "status"),
    ):
        op.create_index(nome, "agendamentos", [coluna])


def downgrade() -> None:
    for nome in (
        "ix_agendamentos_status",
        "ix_agendamentos_fim_em",
        "ix_agendamentos_inicio_em",
        "ix_agendamentos_criado_por_usuario_id",
        "ix_agendamentos_recurso_id",
        "ix_agendamentos_cliente_id",
        "ix_agendamentos_servico_id",
        "ix_agendamentos_profissional_id",
        "ix_agendamentos_empresa_id",
    ):
        op.drop_index(nome, table_name="agendamentos")
    op.drop_table("agendamentos")

    op.drop_index("ix_recursos_agenda_tipo", table_name="recursos_agenda")
    op.drop_index("ix_recursos_agenda_empresa_id", table_name="recursos_agenda")
    op.drop_table("recursos_agenda")

    op.drop_constraint(
        "ck_servicos_duracao_valida", "servicos", type_="check"
    )
    op.drop_column("servicos", "tipo_recurso")
    op.drop_column("servicos", "modo_selecao_recurso")
    op.drop_column("servicos", "requer_recurso")
    op.drop_column("servicos", "duracao_minutos")
