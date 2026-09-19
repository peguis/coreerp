"""permite areas de atuacao configuraveis por empresa

Revision ID: f2a3b4c5d6e7
Revises: e1f2a3b4c5d6
Create Date: 2026-09-19

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import String


revision: str = "f2a3b4c5d6e7"
down_revision: Union[str, Sequence[str], None] = "e1f2a3b4c5d6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "ck_profissionais_area_atuacao",
        "profissionais",
        type_="check",
    )
    op.alter_column(
        "profissionais",
        "area_atuacao",
        existing_type=String(length=20),
        type_=String(length=50),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "profissionais",
        "area_atuacao",
        existing_type=String(length=50),
        type_=String(length=20),
        existing_nullable=False,
    )
    op.create_check_constraint(
        "ck_profissionais_area_atuacao",
        "profissionais",
        "area_atuacao IN ('BARBEARIA', 'TATTOO')",
    )
