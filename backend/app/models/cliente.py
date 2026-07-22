from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.database import Base



class Cliente(Base):

    __tablename__ = "clientes"


    id = Column(
        Integer,
        primary_key=True
    )


    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False,
        index=True
    )


    nome = Column(
        String,
        nullable=False
    )


    cpf_cnpj = Column(
        String,
        nullable=True
    )


    email = Column(
        String,
        nullable=True
    )


    telefone = Column(
        String,
        nullable=True
    )


    ativo = Column(
        Boolean,
        default=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


    empresa = relationship(
        "Empresa",
        back_populates="clientes"
    )


    vendas = relationship(
        "Venda",
        back_populates="cliente"
    )