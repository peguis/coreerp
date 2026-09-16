"""adiciona profissionais e vinculo com usuarios

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-09-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d4e5f6a7b8c9"
down_revision: Union[str, Sequence[str], None] = "c3d4e5f6a7b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "profissionais",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("area_atuacao", sa.String(length=20), nullable=False),
        sa.Column(
            "percentual_padrao",
            sa.Numeric(precision=5, scale=2),
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
            "area_atuacao IN ('BARBEARIA', 'TATTOO')",
            name="ck_profissionais_area_atuacao",
        ),
        sa.CheckConstraint(
            "percentual_padrao >= 0 AND percentual_padrao <= 100",
            name="ck_profissionais_percentual_padrao",
        ),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "empresa_id",
            "usuario_id",
            name="uq_profissionais_empresa_usuario",
        ),
    )
    op.create_index(
        op.f("ix_profissionais_empresa_id"),
        "profissionais",
        ["empresa_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_profissionais_usuario_id"),
        "profissionais",
        ["usuario_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_profissionais_usuario_id"),
        table_name="profissionais",
    )
    op.drop_index(
        op.f("ix_profissionais_empresa_id"),
        table_name="profissionais",
    )
    op.drop_table("profissionais")
