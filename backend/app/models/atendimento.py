from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


if TYPE_CHECKING:
    from app.models.cliente import Cliente
    from app.models.empresa import Empresa
    from app.models.profissional import Profissional
    from app.models.servico import Servico
    from app.models.repasse import RepasseItem


class Atendimento(Base):
    __tablename__ = "atendimentos"
    __table_args__ = (
        CheckConstraint(
            "valor > 0",
            name="ck_atendimentos_valor_positivo",
        ),
        CheckConstraint(
            "forma_pagamento IN "
            "('PIX', 'DINHEIRO', 'CARTAO_DEBITO', 'CARTAO_CREDITO')",
            name="ck_atendimentos_forma_pagamento",
        ),
        CheckConstraint(
            "percentual_profissional >= 0 AND percentual_profissional <= 100",
            name="ck_atendimentos_percentual_profissional",
        ),
        CheckConstraint(
            "valor_profissional >= 0 AND valor_profissional <= valor",
            name="ck_atendimentos_valor_profissional",
        ),
        CheckConstraint(
            "valor_casa >= 0 AND valor_casa <= valor",
            name="ck_atendimentos_valor_casa",
        ),
        CheckConstraint(
            "valor_profissional + valor_casa = valor",
            name="ck_atendimentos_divisao_exata",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"), nullable=False, index=True
    )
    profissional_id: Mapped[int] = mapped_column(
        ForeignKey("profissionais.id"), nullable=False, index=True
    )
    servico_id: Mapped[int] = mapped_column(
        ForeignKey("servicos.id"), nullable=False, index=True
    )
    cliente_id: Mapped[int | None] = mapped_column(
        ForeignKey("clientes.id"), nullable=True, index=True
    )
    valor: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    percentual_profissional: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=False
    )
    valor_profissional: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    valor_casa: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    forma_pagamento: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True
    )
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    realizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(),
        onupdate=func.now()
    )

    empresa: Mapped["Empresa"] = relationship(
        "Empresa", back_populates="atendimentos"
    )
    profissional: Mapped["Profissional"] = relationship(
        "Profissional", back_populates="atendimentos"
    )
    servico: Mapped["Servico"] = relationship(
        "Servico", back_populates="atendimentos"
    )
    cliente: Mapped["Cliente | None"] = relationship(
        "Cliente", back_populates="atendimentos"
    )
    repasse_itens: Mapped[list["RepasseItem"]] = relationship(
        "RepasseItem", back_populates="atendimento"
    )
