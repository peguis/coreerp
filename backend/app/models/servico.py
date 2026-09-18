from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


if TYPE_CHECKING:
    from app.models.atendimento import Atendimento
    from app.models.agendamento import Agendamento
    from app.models.empresa import Empresa


class Servico(Base):
    __tablename__ = "servicos"
    __table_args__ = (
        CheckConstraint(
            "length(trim(nome)) > 0",
            name="ck_servicos_nome_nao_vazio",
        ),
        CheckConstraint(
            "categoria IS NULL OR length(trim(categoria)) > 0",
            name="ck_servicos_categoria_nao_vazia",
        ),
        CheckConstraint(
            "preco_padrao >= 0",
            name="ck_servicos_preco_padrao_nao_negativo",
        ),
        CheckConstraint(
            "duracao_minutos > 0 AND duracao_minutos <= 1440",
            name="ck_servicos_duracao_valida",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        nullable=False,
        index=True,
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    descricao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    categoria: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )

    preco_padrao: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default=text("0.00"),
    )

    duracao_minutos: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=40,
        server_default=text("40"),
    )

    requer_recurso: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )

    tipo_recurso: Mapped[str | None] = mapped_column(
        String(30), nullable=True
    )

    modo_selecao_recurso: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        default="AUTOMATICO",
        server_default=text("'AUTOMATICO'"),
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
        back_populates="servicos",
    )

    atendimentos: Mapped[list["Atendimento"]] = relationship(
        "Atendimento",
        back_populates="servico",
    )

    agendamentos: Mapped[list["Agendamento"]] = relationship(
        "Agendamento",
        back_populates="servico",
    )
