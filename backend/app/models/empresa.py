from datetime import datetime

from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
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
    from app.models.agendamento import Agendamento
    from app.models.recurso_agenda import RecursoAgenda
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

    identidade_codigo: Mapped[str | None] = mapped_column(
        String(40),
        nullable=True,
        index=True,
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

    logo_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    cor_primaria: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    cor_secundaria: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    tema: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    tipo_negocio: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True,
    )

    eh_matriz: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    eh_demo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    criado_por_usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=True,
        index=True,
    )

    demo_expira_em: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
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
        foreign_keys="Usuario.empresa_id",
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

    recursos_agenda: Mapped[list["RecursoAgenda"]] = relationship(
        "RecursoAgenda",
        back_populates="empresa",
        cascade="all, delete-orphan",
    )

    agendamentos: Mapped[list["Agendamento"]] = relationship(
        "Agendamento",
        back_populates="empresa",
        cascade="all, delete-orphan",
    )

    modulos: Mapped[list["EmpresaModulo"]] = relationship(
        "EmpresaModulo",
        back_populates="empresa",
        cascade="all, delete-orphan",
    )
