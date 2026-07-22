from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.database import Base



class MovimentoEstoque(Base):

    __tablename__ = "movimentos_estoque"


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


    produto_id = Column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False,
        index=True
    )


    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True
    )


    tipo = Column(
        String,
        nullable=False
    )


    quantidade = Column(
        Integer,
        nullable=False
    )


    observacao = Column(
        String,
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


    produto = relationship(
        "Produto",
        back_populates="movimentos"
    )


    usuario = relationship(
        "Usuario"
    )


    empresa = relationship(
        "Empresa"
    )