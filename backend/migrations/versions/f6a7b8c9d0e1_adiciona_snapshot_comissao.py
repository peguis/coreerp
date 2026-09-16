"""adiciona snapshot imutavel de comissao aos atendimentos

Revision ID: f6a7b8c9d0e1
Revises: e5f6a7b8c9d0
Create Date: 2026-09-15

"""
from typing import Sequence, Union

from alembic import context, op
import sqlalchemy as sa


revision: str = "f6a7b8c9d0e1"
down_revision: Union[str, Sequence[str], None] = "e5f6a7b8c9d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if not context.is_offline_mode():
        op.execute("LOCK TABLE atendimentos IN ACCESS EXCLUSIVE MODE")
        quantidade = op.get_bind().execute(
            sa.text("SELECT COUNT(*) FROM atendimentos")
        ).scalar_one()
        if quantidade:
            raise RuntimeError(
                "A migration de snapshot exige atendimentos vazios. "
                "Registros historicos devem receber tratamento manual auditavel; "
                "o percentual atual do profissional nao sera usado como historico."
            )

    op.add_column(
        "atendimentos",
        sa.Column(
            "percentual_profissional",
            sa.Numeric(precision=5, scale=2),
            nullable=True,
        ),
    )
    op.add_column(
        "atendimentos",
        sa.Column(
            "valor_profissional",
            sa.Numeric(precision=12, scale=2),
            nullable=True,
        ),
    )
    op.add_column(
        "atendimentos",
        sa.Column(
            "valor_casa",
            sa.Numeric(precision=12, scale=2),
            nullable=True,
        ),
    )

    op.alter_column("atendimentos", "percentual_profissional", nullable=False)
    op.alter_column("atendimentos", "valor_profissional", nullable=False)
    op.alter_column("atendimentos", "valor_casa", nullable=False)

    op.create_check_constraint(
        "ck_atendimentos_percentual_profissional",
        "atendimentos",
        "percentual_profissional >= 0 AND percentual_profissional <= 100",
    )
    op.create_check_constraint(
        "ck_atendimentos_valor_profissional",
        "atendimentos",
        "valor_profissional >= 0 AND valor_profissional <= valor",
    )
    op.create_check_constraint(
        "ck_atendimentos_valor_casa",
        "atendimentos",
        "valor_casa >= 0 AND valor_casa <= valor",
    )
    op.create_check_constraint(
        "ck_atendimentos_divisao_exata",
        "atendimentos",
        "valor_profissional + valor_casa = valor",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_atendimentos_divisao_exata",
        "atendimentos",
        type_="check",
    )
    op.drop_constraint(
        "ck_atendimentos_valor_casa",
        "atendimentos",
        type_="check",
    )
    op.drop_constraint(
        "ck_atendimentos_valor_profissional",
        "atendimentos",
        type_="check",
    )
    op.drop_constraint(
        "ck_atendimentos_percentual_profissional",
        "atendimentos",
        type_="check",
    )
    op.drop_column("atendimentos", "valor_casa")
    op.drop_column("atendimentos", "valor_profissional")
    op.drop_column("atendimentos", "percentual_profissional")
