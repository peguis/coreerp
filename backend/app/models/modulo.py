from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


if TYPE_CHECKING:
    from app.models.empresa import Empresa


class Modulo(Base):
    __tablename__ = "modulos"
    __table_args__ = (
        UniqueConstraint("codigo", name="uq_modulos_codigo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    obrigatorio: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )
    ordem: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    empresas: Mapped[list["EmpresaModulo"]] = relationship(
        "EmpresaModulo",
        back_populates="modulo",
        cascade="all, delete-orphan",
    )


class EmpresaModulo(Base):
    __tablename__ = "empresas_modulos"
    __table_args__ = (
        UniqueConstraint(
            "empresa_id",
            "modulo_id",
            name="uq_empresas_modulos_empresa_modulo",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"), nullable=False, index=True
    )
    modulo_id: Mapped[int] = mapped_column(
        ForeignKey("modulos.id"), nullable=False, index=True
    )
    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
    ativado_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    desativado_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    empresa: Mapped["Empresa"] = relationship(
        "Empresa", back_populates="modulos"
    )
    modulo: Mapped["Modulo"] = relationship(
        "Modulo", back_populates="empresas"
    )
