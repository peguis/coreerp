from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database import Base
from sqlalchemy.orm import relationship


class Venda(Base):

    __tablename__ = "vendas"

    id = Column(
        Integer,
        primary_key=True
    )

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False
    )

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id"),
        nullable=False
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    total = Column(
        Float,
        default=0
    )

    status = Column(
    String,
    nullable=False,
    default="ABERTA"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    itens = relationship(
    "ItemVenda",
    cascade="all, delete",
    lazy="joined"
    )

    cliente = relationship(
    "Cliente"
    )