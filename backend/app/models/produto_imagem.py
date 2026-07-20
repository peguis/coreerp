from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database import Base


class ProdutoImagem(Base):

    __tablename__ = "produto_imagens"


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


    nome_arquivo = Column(
        String,
        nullable=False
    )


    caminho = Column(
        String,
        nullable=False
    )


    principal = Column(
        Boolean,
        default=False
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )