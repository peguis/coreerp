from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func
)

from sqlalchemy.orm import relationship

from app.core.enums import PerfilUsuario

from app.database import Base



class Usuario(Base):

    __tablename__ = "usuarios"


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


    empresa = relationship(
        "Empresa",
        back_populates="usuarios",
        foreign_keys=[empresa_id],
    )


    nome = Column(
        String,
        nullable=False
    )


    email = Column(
        String,
        unique=True,
        nullable=False
    )


    senha = Column(
        String,
        nullable=False
    )


    perfil = Column(
        String,
        nullable=False,
        default=PerfilUsuario.OPERADOR.value
    )


    ativo = Column(
        Boolean,
        default=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


    movimentos_estoque = relationship(
        "MovimentoEstoque",
        back_populates="usuario"
    )


    vendas = relationship(
        "Venda",
        back_populates="usuario"
    )

    lancamentos_financeiros = relationship(
        "LancamentoFinanceiro",
        back_populates="usuario"
    )

    profissional = relationship(
        "Profissional",
        back_populates="usuario",
        uselist=False
    )

    @property
    def area_atuacao(self):
        return self.profissional.area_atuacao if self.profissional else None

    repasses_criados = relationship(
        "Repasse",
        back_populates="created_by_usuario"
    )

    agendamentos_criados = relationship(
        "Agendamento",
        foreign_keys="Agendamento.criado_por_usuario_id",
        back_populates="criado_por",
    )

    agendamentos_cancelados = relationship(
        "Agendamento",
        foreign_keys="Agendamento.cancelado_por_usuario_id",
        back_populates="cancelado_por",
    )

    oportunidades = relationship(
        "Oportunidade",
        foreign_keys="Oportunidade.vendedor_id",
        back_populates="vendedor",
    )
