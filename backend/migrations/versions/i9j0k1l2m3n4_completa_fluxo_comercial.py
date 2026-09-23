"""complete commercial demo and conversion flow

Revision ID: i9j0k1l2m3n4
Revises: h8i9j0k1l2m3
Create Date: 2026-09-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "i9j0k1l2m3n4"
down_revision: Union[str, Sequence[str], None] = "h8i9j0k1l2m3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("empresas", sa.Column("demo_arquivada_em", sa.DateTime(), nullable=True))
    op.add_column("empresas", sa.Column("template_demo", sa.String(length=40), nullable=True))
    op.add_column("empresas", sa.Column("dados_apresentacao", sa.Boolean(), nullable=False, server_default=sa.text("false")))
    op.add_column("empresas", sa.Column("chave_idempotencia", sa.String(length=80), nullable=True))
    op.create_index("ix_empresas_chave_idempotencia", "empresas", ["chave_idempotencia"], unique=True)
    op.add_column("oportunidades", sa.Column("tenant_real_id", sa.Integer(), nullable=True))
    op.create_foreign_key("fk_oportunidades_tenant_real", "oportunidades", "empresas", ["tenant_real_id"], ["id"])
    op.create_index("ix_oportunidades_tenant_real_id", "oportunidades", ["tenant_real_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_oportunidades_tenant_real_id", table_name="oportunidades")
    op.drop_constraint("fk_oportunidades_tenant_real", "oportunidades", type_="foreignkey")
    op.drop_column("oportunidades", "tenant_real_id")
    op.drop_index("ix_empresas_chave_idempotencia", table_name="empresas")
    op.drop_column("empresas", "chave_idempotencia")
    op.drop_column("empresas", "dados_apresentacao")
    op.drop_column("empresas", "template_demo")
    op.drop_column("empresas", "demo_arquivada_em")
