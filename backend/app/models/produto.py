from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
    Text,
    DateTime
)

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
        nullable=False,
        index=True
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
        nullable=True
    )


    codigo_barras = Column(
        String,
        nullable=True
    )


    marca = Column(
        String,
        nullable=True
    )


    unidade = Column(
        String,
        nullable=False,
        default="UN"
    )


    descricao = Column(
        Text,
        nullable=True
    )


    preco = Column(
        Float,
        nullable=False,
        default=0
    )


    estoque = Column(
        Float,
        nullable=False,
        default=0
    )


    estoque_minimo = Column(
        Float,
        nullable=False,
        default=0
    )


    estoque_maximo = Column(
        Float,
        nullable=False,
        default=0
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
        nullable=False,
        default=0
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


    empresa = relationship(
        "Empresa",
        back_populates="produtos"
    )


    imagens = relationship(
        "ProdutoImagem",
        back_populates="produto",
        cascade="all, delete-orphan"
    )


    movimentos = relationship(
        "MovimentoEstoque",
        back_populates="produto",
        cascade="all, delete-orphan"
    )


    itens_venda = relationship(
        "ItemVenda",
        back_populates="produto"
    )