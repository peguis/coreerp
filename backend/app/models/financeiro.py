from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Date,
    DateTime,
    ForeignKey,
    Text,
    CheckConstraint,
    Index,
    text,
)

from sqlalchemy.orm import relationship

from app.database import Base



class LancamentoFinanceiro(Base):

    __tablename__ = "lancamentos_financeiros"
    __table_args__ = (
        CheckConstraint(
            "(origem_tipo IS NULL AND origem_id IS NULL) OR "
            "(origem_tipo IN ('ATENDIMENTO', 'REPASSE') AND origem_id IS NOT NULL)",
            name="ck_lancamentos_financeiros_origem",
        ),
        Index(
            "uq_lancamentos_financeiros_origem_automatica",
            "empresa_id",
            "origem_tipo",
            "origem_id",
            unique=True,
            postgresql_where=text("origem_tipo IS NOT NULL AND origem_id IS NOT NULL"),
            sqlite_where=text("origem_tipo IS NOT NULL AND origem_id IS NOT NULL"),
        ),
    )


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False,
        index=True
    )


    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )


    categoria_id = Column(
        Integer,
        ForeignKey("categorias_financeiras.id"),
        nullable=True,
        index=True
    )


    descricao = Column(
        String(255),
        nullable=False
    )


    valor = Column(
        Numeric(12, 2),
        nullable=False
    )


    origem_tipo = Column(
        String(20),
        nullable=True
    )


    origem_id = Column(
        Integer,
        nullable=True
    )


    forma_pagamento = Column(
        String(20),
        nullable=True
    )


    tipo = Column(
        String(20),
        nullable=False
    )


    data_vencimento = Column(
        Date,
        nullable=False
    )


    data_pagamento = Column(
        DateTime,
        nullable=True
    )


    status = Column(
        String(20),
        default="PENDENTE",
        nullable=False
    )


    observacoes = Column(
        Text,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    empresa = relationship(
        "Empresa",
        back_populates="lancamentos_financeiros"
    )


    usuario = relationship(
        "Usuario",
        back_populates="lancamentos_financeiros"
    )


    categoria = relationship(
        "CategoriaFinanceira",
        back_populates="lancamentos"
    )
