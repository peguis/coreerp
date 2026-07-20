from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

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

    categoria = Column(
        String,
        nullable=True
    )

    codigo_interno = Column(
        String,
        unique=False,
        nullable=True
    )

    codigo_barras = Column(
        String,
        unique=False,
        nullable=True
    )

    marca = Column(
        String,
        nullable=True
    )

    unidade = Column(
        String,
        default="UN"
    )

    descricao = Column(
        Text,
        nullable=True
    )

    preco = Column(
        Float,
        nullable=False
    )

    estoque = Column(
        Float,
        default=0,
        nullable=False
        
    )
    estoque_minimo = Column(
        Float,
        default=0,
        nullable=False
    )

    estoque_maximo = Column(
        Float,
        default=0,
        nullable=False
    )
    
    peso = Column(
        Float,
        nullable=True
    )

    altura = Column(
        Float,
        nullable=True
    )

    largura = Column(
        Float,
        nullable=True
    )

    comprimento = Column(
        Float,
        nullable=True
    )

    localizacao = Column(
        String,
        nullable=True
    )

    custo_medio = Column(
        Float,
        default=0,
        nullable=False
    )

    ultima_entrada = Column(
        DateTime,
        nullable=True
    )

    ultima_saida = Column(
        DateTime,
        nullable=True
    )
       

    ativo = Column(
        Boolean,
        default=True
    )

    imagens = relationship(
    "ProdutoImagem",
    cascade="all, delete-orphan",
    backref="produto"
    )