"""adiciona campos profissionais produto

Revision ID: b2e9997eb0cc
Revises: b71844930427
Create Date: 2026-07-20 00:12:54.134678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2e9997eb0cc'
down_revision: Union[str, Sequence[str], None] = 'b71844930427'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        'produtos',
        sa.Column(
            'peso',
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        'produtos',
        sa.Column(
            'altura',
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        'produtos',
        sa.Column(
            'largura',
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        'produtos',
        sa.Column(
            'comprimento',
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        'produtos',
        sa.Column(
            'localizacao',
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        'produtos',
        sa.Column(
            'custo_medio',
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        'produtos',
        sa.Column(
            'ultima_entrada',
            sa.DateTime(),
            nullable=True
        )
    )

    op.add_column(
        'produtos',
        sa.Column(
            'ultima_saida',
            sa.DateTime(),
            nullable=True
        )
    )


def downgrade() -> None:

    op.drop_column('produtos', 'ultima_saida')
    op.drop_column('produtos', 'ultima_entrada')
    op.drop_column('produtos', 'custo_medio')
    op.drop_column('produtos', 'localizacao')
    op.drop_column('produtos', 'comprimento')
    op.drop_column('produtos', 'largura')
    op.drop_column('produtos', 'altura')
    op.drop_column('produtos', 'peso')
