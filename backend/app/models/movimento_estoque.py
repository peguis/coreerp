from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

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
        nullable=False
    )

    produto_id = Column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
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
        server_default=func.now()
    )