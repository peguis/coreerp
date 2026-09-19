"""cria catalogo de modulos e configuracao visual da empresa

Revision ID: e1f2a3b4c5d6
Revises: d9e0f1a2b3c4
Create Date: 2026-09-19

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e1f2a3b4c5d6"
down_revision: Union[str, Sequence[str], None] = "d9e0f1a2b3c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


MODULOS = (
    ("dashboard", "Dashboard", "Resumo executivo da operação", 10),
    ("agenda", "Agenda", "Agendamentos e disponibilidade", 20),
    ("clientes", "Clientes", "Cadastro e histórico de clientes", 30),
    ("servicos", "Serviços", "Catálogo de serviços e preços", 40),
    ("profissionais", "Profissionais", "Equipe e áreas de atuação", 50),
    ("recursos", "Recursos físicos", "Cadeiras, macas e estações", 60),
    ("atendimentos", "Atendimentos", "Registro de serviços realizados", 70),
    ("repasses", "Repasses e comissões", "Produção e valores de profissionais", 80),
    ("financeiro", "Financeiro", "Lançamentos financeiros", 90),
    ("produtos", "Produtos", "Catálogo de produtos", 100),
    ("estoque", "Estoque", "Movimentação e saldo de estoque", 110),
    ("vendas", "Vendas", "Vendas de produtos", 120),
)


def upgrade() -> None:
    op.add_column("empresas", sa.Column("logo_url", sa.Text(), nullable=True))
    op.add_column("empresas", sa.Column("cor_primaria", sa.String(length=20), nullable=True))
    op.add_column("empresas", sa.Column("cor_secundaria", sa.String(length=20), nullable=True))
    op.add_column("empresas", sa.Column("tema", sa.String(length=20), nullable=True))
    op.add_column("empresas", sa.Column("tipo_negocio", sa.String(length=80), nullable=True))

    op.create_table(
        "modulos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("codigo", sa.String(length=50), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("obrigatorio", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("ordem", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("codigo", name="uq_modulos_codigo"),
    )
    op.create_index("ix_modulos_codigo", "modulos", ["codigo"], unique=False)

    op.create_table(
        "empresas_modulos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("modulo_id", sa.Integer(), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("ativado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("desativado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["modulo_id"], ["modulos.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "empresa_id",
            "modulo_id",
            name="uq_empresas_modulos_empresa_modulo",
        ),
    )
    op.create_index("ix_empresas_modulos_empresa_id", "empresas_modulos", ["empresa_id"], unique=False)
    op.create_index("ix_empresas_modulos_modulo_id", "empresas_modulos", ["modulo_id"], unique=False)

    catalogo = sa.table(
        "modulos",
        sa.column("codigo", sa.String()),
        sa.column("nome", sa.String()),
        sa.column("descricao", sa.Text()),
        sa.column("obrigatorio", sa.Boolean()),
        sa.column("ordem", sa.Integer()),
    )
    op.bulk_insert(
        catalogo,
        [
            {
                "codigo": codigo,
                "nome": nome,
                "descricao": descricao,
                "obrigatorio": False,
                "ordem": ordem,
            }
            for codigo, nome, descricao, ordem in MODULOS
        ],
    )

    # Use INSERT ... SELECT so the migration also supports Alembic offline SQL
    # generation and does not load tenant IDs into the migration process.
    op.execute(
        sa.text(
            "INSERT INTO empresas_modulos (empresa_id, modulo_id, ativo) "
            "SELECT empresas.id, modulos.id, true "
            "FROM empresas CROSS JOIN modulos"
        )
    )


def downgrade() -> None:
    op.drop_index("ix_empresas_modulos_modulo_id", table_name="empresas_modulos")
    op.drop_index("ix_empresas_modulos_empresa_id", table_name="empresas_modulos")
    op.drop_table("empresas_modulos")
    op.drop_index("ix_modulos_codigo", table_name="modulos")
    op.drop_table("modulos")
    op.drop_column("empresas", "tipo_negocio")
    op.drop_column("empresas", "tema")
    op.drop_column("empresas", "cor_secundaria")
    op.drop_column("empresas", "cor_primaria")
    op.drop_column("empresas", "logo_url")
