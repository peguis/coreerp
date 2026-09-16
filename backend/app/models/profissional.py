from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


if TYPE_CHECKING:
    from app.models.atendimento import Atendimento
    from app.models.empresa import Empresa
    from app.models.usuario import Usuario
    from app.models.repasse import Repasse


class Profissional(Base):
    __tablename__ = "profissionais"
    __table_args__ = (
        UniqueConstraint(
            "empresa_id",
            "usuario_id",
            name="uq_profissionais_empresa_usuario",
        ),
        CheckConstraint(
            "area_atuacao IN ('BARBEARIA', 'TATTOO')",
            name="ck_profissionais_area_atuacao",
        ),
        CheckConstraint(
            "percentual_padrao >= 0 AND percentual_padrao <= 100",
            name="ck_profissionais_percentual_padrao",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        nullable=False,
        index=True,
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )

    area_atuacao: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    percentual_padrao: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default=text("0.00"),
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    empresa: Mapped["Empresa"] = relationship(
        "Empresa",
        back_populates="profissionais",
    )

    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="profissional",
    )

    atendimentos: Mapped[list["Atendimento"]] = relationship(
        "Atendimento",
        back_populates="profissional",
    )

    repasses: Mapped[list["Repasse"]] = relationship(
        "Repasse",
        back_populates="profissional",
    )
