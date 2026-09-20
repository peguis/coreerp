"""cria auditoria administrativa por empresa

Revision ID: a3b4c5d6e7f8
Revises: f2a3b4c5d6e7
Create Date: 2026-09-19

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a3b4c5d6e7f8"
down_revision: Union[str, Sequence[str], None] = "f2a3b4c5d6e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "auditorias",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=True),
        sa.Column("acao", sa.String(length=50), nullable=False),
        sa.Column("recurso", sa.String(length=80), nullable=False),
        sa.Column("recurso_id", sa.Integer(), nullable=True),
        sa.Column("detalhes", sa.JSON(), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_auditorias_empresa_id", "auditorias", ["empresa_id"], unique=False)
    op.create_index("ix_auditorias_usuario_id", "auditorias", ["usuario_id"], unique=False)
    op.create_index("ix_auditorias_acao", "auditorias", ["acao"], unique=False)
    op.create_index("ix_auditorias_recurso", "auditorias", ["recurso"], unique=False)
    op.create_index("ix_auditorias_recurso_id", "auditorias", ["recurso_id"], unique=False)
    op.create_index("ix_auditorias_criado_em", "auditorias", ["criado_em"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_auditorias_criado_em", table_name="auditorias")
    op.drop_index("ix_auditorias_recurso_id", table_name="auditorias")
    op.drop_index("ix_auditorias_recurso", table_name="auditorias")
    op.drop_index("ix_auditorias_acao", table_name="auditorias")
    op.drop_index("ix_auditorias_usuario_id", table_name="auditorias")
    op.drop_index("ix_auditorias_empresa_id", table_name="auditorias")
    op.drop_table("auditorias")
