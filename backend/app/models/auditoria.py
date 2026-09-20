from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class RegistroAuditoria(Base):
    __tablename__ = "auditorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"), nullable=False, index=True
    )
    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True, index=True
    )
    acao: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    recurso: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    recurso_id: Mapped[int | None] = mapped_column(nullable=True, index=True)
    detalhes: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )
