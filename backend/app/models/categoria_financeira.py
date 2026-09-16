from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database.database import Base



class CategoriaFinanceira(Base):

    __tablename__ = "categorias_financeiras"
    __table_args__ = (
        Index(
            "uq_categorias_financeiras_chave_sistema",
            "empresa_id",
            "chave_sistema",
            unique=True,
            postgresql_where=text("chave_sistema IS NOT NULL"),
            sqlite_where=text("chave_sistema IS NOT NULL"),
        ),
    )


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )


    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        nullable=False,
        index=True
    )


    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


    tipo: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )


    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


    empresa = relationship(
        "Empresa",
        back_populates="categorias_financeiras"
    )


    lancamentos = relationship(
        "LancamentoFinanceiro",
        back_populates="categoria"
    )


    chave_sistema: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )
