from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey

from app.database import Base


class Produto(Base):

    __tablename__ = "produtos"

    id = Column(
        Integer,
        primary_key=True
    )

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False
    )

    nome = Column(
        String,
        nullable=False
    )

    preco = Column(
        Float,
        nullable=False
    )

    estoque = Column(
        Integer,
        default=0
    )

    ativo = Column(
        Boolean,
        default=True
    )