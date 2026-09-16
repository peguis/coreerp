from datetime import datetime

from typing import TYPE_CHECKING

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


if TYPE_CHECKING:

    from app.models.usuario import Usuario
    from app.models.venda import Venda
    from app.models.produto import Produto
    from app.models.cliente import Cliente
    from app.models.movimento_estoque import MovimentoEstoque
    from app.models.produto_imagem import ProdutoImagem
    from app.models.financeiro import LancamentoFinanceiro
    from app.models.categoria_financeira import CategoriaFinanceira
    from app.models.servico import Servico
    from app.models.profissional import Profissional
    from app.models.atendimento import Atendimento
    from app.models.repasse import Repasse, RepasseItem



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


    lancamentos_financeiros: Mapped[list["LancamentoFinanceiro"]] = relationship(
        "LancamentoFinanceiro",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )


    categorias_financeiras: Mapped[list["CategoriaFinanceira"]] = relationship(
        "CategoriaFinanceira",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )


    servicos: Mapped[list["Servico"]] = relationship(
        "Servico",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )


    profissionais: Mapped[list["Profissional"]] = relationship(
        "Profissional",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )


    atendimentos: Mapped[list["Atendimento"]] = relationship(
        "Atendimento",
        back_populates="empresa"
    )

    repasses: Mapped[list["Repasse"]] = relationship(
        "Repasse",
        back_populates="empresa"
    )

    repasse_itens: Mapped[list["RepasseItem"]] = relationship(
        "RepasseItem",
        back_populates="empresa"
    )
