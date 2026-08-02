from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    Text,
)

from sqlalchemy.orm import relationship

from app.database import Base



class LancamentoFinanceiro(Base):

    __tablename__ = "lancamentos_financeiros"


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
        Float,
        nullable=False
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