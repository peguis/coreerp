from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database.database import Base



class Empresa(Base):

    __tablename__ = "empresas"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )


    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


    cnpj: Mapped[str] = mapped_column(
        String(18),
        unique=True,
        nullable=False
    )


    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )


    telefone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )


    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


    usuarios: Mapped[list["Usuario"]] = relationship(
        "Usuario",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )


    vendas: Mapped[list["Venda"]] = relationship(
        "Venda",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )


    produtos: Mapped[list["Produto"]] = relationship(
        "Produto",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )


    clientes: Mapped[list["Cliente"]] = relationship(
        "Cliente",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )


    movimentos_estoque: Mapped[list["MovimentoEstoque"]] = relationship(
        "MovimentoEstoque",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )


    imagens_produto: Mapped[list["ProdutoImagem"]] = relationship(
        "ProdutoImagem",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )