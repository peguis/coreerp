from datetime import date, datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


if TYPE_CHECKING:
    from app.models.empresa import Empresa
    from app.models.usuario import Usuario


class Oportunidade(Base):
    __tablename__ = "oportunidades"

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"), nullable=False, index=True
    )
    vendedor_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), nullable=False, index=True
    )
    nome_negocio_contato: Mapped[str] = mapped_column(String(150), nullable=False)
    pessoa_responsavel: Mapped[str | None] = mapped_column(String(150), nullable=True)
    telefone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    canal_contato: Mapped[str | None] = mapped_column(String(80), nullable=True)
    cidade_regiao: Mapped[str | None] = mapped_column(String(120), nullable=True)
    tipo_negocio: Mapped[str | None] = mapped_column(String(80), nullable=True)
    origem: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="NOVO")
    proxima_acao: Mapped[str | None] = mapped_column(String(180), nullable=True)
    proximo_contato: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    modulos_interesse: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    tenant_demo_id: Mapped[int | None] = mapped_column(
        ForeignKey("empresas.id"), nullable=True, index=True
    )
    ultima_interacao_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    conversao_solicitada_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    conversao_solicitada_por_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )
    convertido_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    convertido_por_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )

    vendedor: Mapped["Usuario"] = relationship(
        "Usuario",
        foreign_keys=[vendedor_id],
        back_populates="oportunidades",
    )
    empresa_matriz: Mapped["Empresa"] = relationship(
        "Empresa", foreign_keys=[empresa_id]
    )
    tenant_demo: Mapped["Empresa | None"] = relationship(
        "Empresa", foreign_keys=[tenant_demo_id]
    )
    interacoes: Mapped[list["OportunidadeInteracao"]] = relationship(
        "OportunidadeInteracao",
        back_populates="oportunidade",
        cascade="all, delete-orphan",
        order_by="OportunidadeInteracao.criado_em.desc()",
    )


class OportunidadeInteracao(Base):
    __tablename__ = "oportunidades_interacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    oportunidade_id: Mapped[int] = mapped_column(
        ForeignKey("oportunidades.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), nullable=False, index=True
    )
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    proxima_acao: Mapped[str | None] = mapped_column(String(180), nullable=True)
    proximo_contato: Mapped[date | None] = mapped_column(Date, nullable=True)
    detalhes: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )

    oportunidade: Mapped["Oportunidade"] = relationship(
        "Oportunidade", back_populates="interacoes"
    )
    usuario: Mapped["Usuario"] = relationship(
        "Usuario", foreign_keys=[usuario_id]
    )
