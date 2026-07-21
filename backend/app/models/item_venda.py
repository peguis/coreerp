from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class ItemVenda(Base):

    __tablename__ = "itens_venda"


    id = Column(
        Integer,
        primary_key=True
    )


    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False
    )


    venda_id = Column(
        Integer,
        ForeignKey("vendas.id"),
        nullable=False
    )


    produto_id = Column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False
    )


    quantidade = Column(
        Integer,
        nullable=False
    )


    preco_unitario = Column(
        Float,
        nullable=False
    )


    subtotal = Column(
        Float,
        nullable=False
    )


    produto = relationship(
        "Produto"
    )