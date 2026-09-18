from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


if TYPE_CHECKING:
    from app.models.agendamento import Agendamento
    from app.models.empresa import Empresa


class RecursoAgenda(Base):
    __tablename__ = "recursos_agenda"
    __table_args__ = (
        UniqueConstraint(
            "empresa_id",
            "nome",
            name="uq_recursos_agenda_empresa_nome",
        ),
        CheckConstraint(
            "length(trim(nome)) > 0",
            name="ck_recursos_agenda_nome_nao_vazio",
        ),
        CheckConstraint(
            "length(trim(tipo)) > 0",
            name="ck_recursos_agenda_tipo_nao_vazio",
        ),
        CheckConstraint(
            "status IN ('ATIVO', 'INATIVO', 'MANUTENCAO')",
            name="ck_recursos_agenda_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"), nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ATIVO",
        server_default=text("'ATIVO'"),
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    empresa: Mapped["Empresa"] = relationship(
        "Empresa", back_populates="recursos_agenda"
    )
    agendamentos: Mapped[list["Agendamento"]] = relationship(
        "Agendamento", back_populates="recurso"
    )

    @property
    def disponivel(self) -> bool:
        return self.ativo and self.status == "ATIVO"
