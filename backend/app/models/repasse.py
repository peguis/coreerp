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
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


if TYPE_CHECKING:
    from app.models.atendimento import Atendimento
    from app.models.empresa import Empresa
    from app.models.profissional import Profissional
    from app.models.usuario import Usuario


class Repasse(Base):
    __tablename__ = "repasses"
    __table_args__ = (
        CheckConstraint("valor > 0", name="ck_repasses_valor_positivo"),
        CheckConstraint(
            "forma_pagamento IN ('PIX', 'DINHEIRO', 'TRANSFERENCIA')",
            name="ck_repasses_forma_pagamento",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"), nullable=False, index=True
    )
    profissional_id: Mapped[int] = mapped_column(
        ForeignKey("profissionais.id"), nullable=False, index=True
    )
    created_by_usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), nullable=False, index=True
    )
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    forma_pagamento: Mapped[str] = mapped_column(String(20), nullable=False)
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    pago_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    empresa: Mapped["Empresa"] = relationship(
        "Empresa", back_populates="repasses"
    )
    profissional: Mapped["Profissional"] = relationship(
        "Profissional", back_populates="repasses"
    )
    created_by_usuario: Mapped["Usuario"] = relationship(
        "Usuario", back_populates="repasses_criados"
    )
    itens: Mapped[list["RepasseItem"]] = relationship(
        "RepasseItem", back_populates="repasse", lazy="selectin"
    )


class RepasseItem(Base):
    __tablename__ = "repasse_itens"
    __table_args__ = (
        UniqueConstraint(
            "repasse_id",
            "atendimento_id",
            name="uq_repasse_itens_repasse_atendimento",
        ),
        CheckConstraint(
            "valor > 0", name="ck_repasse_itens_valor_positivo"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"), nullable=False, index=True
    )
    repasse_id: Mapped[int] = mapped_column(
        ForeignKey("repasses.id"), nullable=False, index=True
    )
    atendimento_id: Mapped[int] = mapped_column(
        ForeignKey("atendimentos.id"), nullable=False, index=True
    )
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    empresa: Mapped["Empresa"] = relationship(
        "Empresa", back_populates="repasse_itens"
    )
    repasse: Mapped["Repasse"] = relationship(
        "Repasse", back_populates="itens"
    )
    atendimento: Mapped["Atendimento"] = relationship(
        "Atendimento", back_populates="repasse_itens"
    )
