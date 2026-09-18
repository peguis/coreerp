from datetime import datetime
from typing import TYPE_CHECKING

from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


if TYPE_CHECKING:
    from app.models.cliente import Cliente
    from app.models.empresa import Empresa
    from app.models.profissional import Profissional
    from app.models.recurso_agenda import RecursoAgenda
    from app.models.servico import Servico
    from app.models.usuario import Usuario


class Agendamento(Base):
    __tablename__ = "agendamentos"
    __table_args__ = (
        CheckConstraint(
            "fim_em > inicio_em",
            name="ck_agendamentos_fim_depois_inicio",
        ),
        CheckConstraint(
            "duracao_minutos > 0 AND duracao_minutos <= 1440",
            name="ck_agendamentos_duracao_valida",
        ),
        CheckConstraint(
            "preco_aplicado >= 0",
            name="ck_agendamentos_preco_valido",
        ),
        CheckConstraint(
            "status IN ('AGENDADO', 'CONFIRMADO', 'CONCLUIDO', 'CANCELADO', 'NAO_COMPARECEU')",
            name="ck_agendamentos_status",
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
    cliente_avulso_nome: Mapped[str | None] = mapped_column(
        String(150), nullable=True
    )
    recurso_id: Mapped[int | None] = mapped_column(
        ForeignKey("recursos_agenda.id"), nullable=True, index=True
    )
    criado_por_usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), nullable=False, index=True
    )
    inicio_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    fim_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    duracao_minutos: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    preco_aplicado: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default=text("0.00"),
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="AGENDADO",
        server_default="AGENDADO",
        index=True,
    )
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    motivo_cancelamento: Mapped[str | None] = mapped_column(Text, nullable=True)
    cancelado_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    cancelado_por_usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
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
        "Empresa", back_populates="agendamentos"
    )
    profissional: Mapped["Profissional"] = relationship(
        "Profissional", back_populates="agendamentos"
    )
    servico: Mapped["Servico"] = relationship(
        "Servico", back_populates="agendamentos"
    )
    cliente: Mapped["Cliente | None"] = relationship(
        "Cliente", back_populates="agendamentos"
    )
    recurso: Mapped["RecursoAgenda | None"] = relationship(
        "RecursoAgenda", back_populates="agendamentos"
    )
    criado_por: Mapped["Usuario"] = relationship(
        "Usuario",
        foreign_keys=[criado_por_usuario_id],
        back_populates="agendamentos_criados",
    )
    cancelado_por: Mapped["Usuario | None"] = relationship(
        "Usuario",
        foreign_keys=[cancelado_por_usuario_id],
        back_populates="agendamentos_cancelados",
    )
