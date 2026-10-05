from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Text,
    Index
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.database import Base



class Venda(Base):

    __tablename__ = "vendas"

    __table_args__ = (
        Index(
            "uq_vendas_empresa_chave_idempotencia",
            "empresa_id",
            "chave_idempotencia",
            unique=True
        ),
    )


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


    estoque_baixado = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1"
    )


    origem = Column(
        String(30),
        nullable=False,
        default="ERP",
        server_default="ERP"
    )


    pedido_externo_id = Column(
        String(100),
        nullable=True,
        index=True
    )


    chave_idempotencia = Column(
        String(80),
        nullable=True,
        index=True
    )


    observacoes = Column(
        Text,
        nullable=True
    )


    endereco_entrega = Column(
        Text,
        nullable=True
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
