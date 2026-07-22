from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.database import Base



class Venda(Base):

    __tablename__ = "vendas"


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


    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id"),
        nullable=False,
        index=True
    )


    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True
    )


    total = Column(
        Float,
        nullable=False,
        default=0
    )


    status = Column(
        String,
        nullable=False,
        default="ABERTA"
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


    empresa = relationship(
        "Empresa",
        back_populates="vendas"
    )


    cliente = relationship(
        "Cliente",
        back_populates="vendas"
    )


    usuario = relationship(
        "Usuario",
        back_populates="vendas"
    )


    itens = relationship(
        "ItemVenda",
        back_populates="venda",
        cascade="all, delete-orphan",
        lazy="joined"
    )