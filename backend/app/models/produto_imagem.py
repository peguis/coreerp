from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.database import Base



class ProdutoImagem(Base):

    __tablename__ = "produto_imagens"


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


    produto_id = Column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False,
        index=True
    )


    nome_arquivo = Column(
        String(255),
        nullable=False
    )


    caminho = Column(
        String(500),
        nullable=False
    )


    principal = Column(
        Boolean,
        default=False,
        nullable=False
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )