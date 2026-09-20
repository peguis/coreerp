"""adiciona vendedores pegs e oportunidades comerciais

Revision ID: h8i9j0k1l2m3
Revises: a3b4c5d6e7f8, g7h8i9j0k1l2
Create Date: 2026-09-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "h8i9j0k1l2m3"
down_revision: Union[str, Sequence[str], None] = ("a3b4c5d6e7f8", "g7h8i9j0k1l2")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "empresas",
        sa.Column("eh_matriz", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.add_column(
        "empresas",
        sa.Column("eh_demo", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.add_column(
        "empresas",
        sa.Column("criado_por_usuario_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "empresas",
        sa.Column("demo_expira_em", sa.DateTime(), nullable=True),
    )
    op.create_foreign_key(
        "fk_empresas_criado_por_usuario",
        "empresas",
        "usuarios",
        ["criado_por_usuario_id"],
        ["id"],
    )
    op.create_index(
        "ix_empresas_criado_por_usuario_id",
        "empresas",
        ["criado_por_usuario_id"],
        unique=False,
    )
    op.execute(
        sa.text(
            "UPDATE empresas SET eh_matriz = true WHERE id IN ("
            "SELECT DISTINCT empresa_id FROM usuarios WHERE perfil = 'pegs_admin'"
            ")"
        )
    )

    op.create_table(
        "oportunidades",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("vendedor_id", sa.Integer(), nullable=False),
        sa.Column("nome_negocio_contato", sa.String(length=150), nullable=False),
        sa.Column("pessoa_responsavel", sa.String(length=150), nullable=True),
        sa.Column("telefone", sa.String(length=30), nullable=True),
        sa.Column("email", sa.String(length=150), nullable=True),
        sa.Column("canal_contato", sa.String(length=80), nullable=True),
        sa.Column("cidade_regiao", sa.String(length=120), nullable=True),
        sa.Column("tipo_negocio", sa.String(length=80), nullable=True),
        sa.Column("origem", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="NOVO"),
        sa.Column("proxima_acao", sa.String(length=180), nullable=True),
        sa.Column("proximo_contato", sa.Date(), nullable=True),
        sa.Column("observacoes", sa.Text(), nullable=True),
        sa.Column("modulos_interesse", sa.JSON(), nullable=True),
        sa.Column("tenant_demo_id", sa.Integer(), nullable=True),
        sa.Column("ultima_interacao_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("conversao_solicitada_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("conversao_solicitada_por_id", sa.Integer(), nullable=True),
        sa.Column("convertido_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("convertido_por_id", sa.Integer(), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["vendedor_id"], ["usuarios.id"]),
        sa.ForeignKeyConstraint(["tenant_demo_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["conversao_solicitada_por_id"], ["usuarios.id"]),
        sa.ForeignKeyConstraint(["convertido_por_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_oportunidades_empresa_id", "oportunidades", ["empresa_id"], unique=False)
    op.create_index("ix_oportunidades_vendedor_id", "oportunidades", ["vendedor_id"], unique=False)
    op.create_index("ix_oportunidades_tenant_demo_id", "oportunidades", ["tenant_demo_id"], unique=False)
    op.create_index("ix_oportunidades_criado_em", "oportunidades", ["criado_em"], unique=False)

    op.create_table(
        "oportunidades_interacoes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("oportunidade_id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column("proxima_acao", sa.String(length=180), nullable=True),
        sa.Column("proximo_contato", sa.Date(), nullable=True),
        sa.Column("detalhes", sa.JSON(), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["oportunidade_id"], ["oportunidades.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_oportunidades_interacoes_oportunidade_id", "oportunidades_interacoes", ["oportunidade_id"], unique=False)
    op.create_index("ix_oportunidades_interacoes_usuario_id", "oportunidades_interacoes", ["usuario_id"], unique=False)
    op.create_index("ix_oportunidades_interacoes_criado_em", "oportunidades_interacoes", ["criado_em"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_oportunidades_interacoes_criado_em", table_name="oportunidades_interacoes")
    op.drop_index("ix_oportunidades_interacoes_usuario_id", table_name="oportunidades_interacoes")
    op.drop_index("ix_oportunidades_interacoes_oportunidade_id", table_name="oportunidades_interacoes")
    op.drop_table("oportunidades_interacoes")
    op.drop_index("ix_oportunidades_criado_em", table_name="oportunidades")
    op.drop_index("ix_oportunidades_tenant_demo_id", table_name="oportunidades")
    op.drop_index("ix_oportunidades_vendedor_id", table_name="oportunidades")
    op.drop_index("ix_oportunidades_empresa_id", table_name="oportunidades")
    op.drop_table("oportunidades")
    op.drop_index("ix_empresas_criado_por_usuario_id", table_name="empresas")
    op.drop_constraint("fk_empresas_criado_por_usuario", "empresas", type_="foreignkey")
    op.drop_column("empresas", "demo_expira_em")
    op.drop_column("empresas", "criado_por_usuario_id")
    op.drop_column("empresas", "eh_demo")
    op.drop_column("empresas", "eh_matriz")
