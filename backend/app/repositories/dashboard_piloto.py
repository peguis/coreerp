from datetime import datetime

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.atendimento import Atendimento
from app.models.financeiro import LancamentoFinanceiro
from app.models.profissional import Profissional
from app.models.repasse import Repasse, RepasseItem
from app.models.servico import Servico
from app.models.usuario import Usuario


def _filtro_periodo(campo, inicio: datetime, fim_exclusivo: datetime):
    return campo >= inicio, campo < fim_exclusivo


def obter_totais_producao(
    db: Session, empresa_id: int, inicio: datetime, fim_exclusivo: datetime
):
    return (
        db.query(
            func.count(Atendimento.id).label("total_atendimentos"),
            func.coalesce(func.sum(Atendimento.valor), 0).label(
                "faturamento_bruto"
            ),
            func.coalesce(func.sum(Atendimento.valor_profissional), 0).label(
                "valor_profissionais"
            ),
            func.coalesce(func.sum(Atendimento.valor_casa), 0).label(
                "valor_casa"
            ),
        )
        .filter(
            Atendimento.empresa_id == empresa_id,
            *_filtro_periodo(Atendimento.realizado_em, inicio, fim_exclusivo),
        )
        .one()
    )


def obter_total_repassado(
    db: Session, empresa_id: int, inicio: datetime, fim_exclusivo: datetime
):
    return (
        db.query(func.coalesce(func.sum(Repasse.valor), 0))
        .filter(
            Repasse.empresa_id == empresa_id,
            *_filtro_periodo(Repasse.pago_em, inicio, fim_exclusivo),
        )
        .scalar()
    )


def _itens_repassados_por_atendimento(db: Session, empresa_id: int):
    return (
        db.query(
            RepasseItem.atendimento_id.label("atendimento_id"),
            func.sum(RepasseItem.valor).label("valor_repassado"),
        )
        .filter(RepasseItem.empresa_id == empresa_id)
        .group_by(RepasseItem.atendimento_id)
        .subquery()
    )


def obter_total_pendente(
    db: Session, empresa_id: int, inicio: datetime, fim_exclusivo: datetime
):
    itens = _itens_repassados_por_atendimento(db, empresa_id)
    return (
        db.query(
            func.coalesce(
                func.sum(
                    Atendimento.valor_profissional
                    - func.coalesce(itens.c.valor_repassado, 0)
                ),
                0,
            )
        )
        .outerjoin(itens, itens.c.atendimento_id == Atendimento.id)
        .filter(
            Atendimento.empresa_id == empresa_id,
            *_filtro_periodo(Atendimento.realizado_em, inicio, fim_exclusivo),
        )
        .scalar()
    )


def obter_caixa_piloto(
    db: Session, empresa_id: int, inicio: datetime, fim_exclusivo: datetime
):
    return (
        db.query(
            func.coalesce(
                func.sum(
                    case(
                        (
                            (LancamentoFinanceiro.origem_tipo == "ATENDIMENTO")
                            & (LancamentoFinanceiro.tipo == "RECEITA")
                            & (LancamentoFinanceiro.status == "RECEBIDO"),
                            LancamentoFinanceiro.valor,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label("entradas"),
            func.coalesce(
                func.sum(
                    case(
                        (
                            (LancamentoFinanceiro.origem_tipo == "REPASSE")
                            & (LancamentoFinanceiro.tipo == "DESPESA")
                            & (LancamentoFinanceiro.status == "PAGO"),
                            LancamentoFinanceiro.valor,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label("saidas"),
        )
        .filter(
            LancamentoFinanceiro.empresa_id == empresa_id,
            LancamentoFinanceiro.origem_tipo.in_(("ATENDIMENTO", "REPASSE")),
            LancamentoFinanceiro.data_pagamento.is_not(None),
            *_filtro_periodo(
                LancamentoFinanceiro.data_pagamento, inicio, fim_exclusivo
            ),
        )
        .one()
    )


def listar_desempenho_profissionais(
    db: Session,
    empresa_id: int,
    inicio: datetime,
    fim_exclusivo: datetime,
    profissional_id: int | None = None,
):
    producao = (
        db.query(
            Atendimento.profissional_id.label("profissional_id"),
            func.count(Atendimento.id).label("total_atendimentos"),
            func.sum(Atendimento.valor).label("faturamento_bruto"),
            func.sum(Atendimento.valor_profissional).label(
                "valor_profissional"
            ),
            func.sum(Atendimento.valor_casa).label("valor_casa"),
        )
        .filter(
            Atendimento.empresa_id == empresa_id,
            *_filtro_periodo(Atendimento.realizado_em, inicio, fim_exclusivo),
        )
        .group_by(Atendimento.profissional_id)
        .subquery()
    )
    repassado = (
        db.query(
            Repasse.profissional_id.label("profissional_id"),
            func.sum(Repasse.valor).label("total_repassado"),
        )
        .filter(
            Repasse.empresa_id == empresa_id,
            *_filtro_periodo(Repasse.pago_em, inicio, fim_exclusivo),
        )
        .group_by(Repasse.profissional_id)
        .subquery()
    )
    itens = _itens_repassados_por_atendimento(db, empresa_id)
    pendente = (
        db.query(
            Atendimento.profissional_id.label("profissional_id"),
            func.sum(
                Atendimento.valor_profissional
                - func.coalesce(itens.c.valor_repassado, 0)
            ).label("total_pendente"),
        )
        .outerjoin(itens, itens.c.atendimento_id == Atendimento.id)
        .filter(
            Atendimento.empresa_id == empresa_id,
            *_filtro_periodo(Atendimento.realizado_em, inicio, fim_exclusivo),
        )
        .group_by(Atendimento.profissional_id)
        .subquery()
    )
    query = (
        db.query(
            Profissional.id.label("profissional_id"),
            Usuario.nome,
            Profissional.area_atuacao,
            func.coalesce(producao.c.total_atendimentos, 0).label(
                "total_atendimentos"
            ),
            func.coalesce(producao.c.faturamento_bruto, 0).label(
                "faturamento_bruto"
            ),
            func.coalesce(producao.c.valor_profissional, 0).label(
                "valor_profissional"
            ),
            func.coalesce(producao.c.valor_casa, 0).label("valor_casa"),
            func.coalesce(repassado.c.total_repassado, 0).label(
                "total_repassado"
            ),
            func.coalesce(pendente.c.total_pendente, 0).label(
                "total_pendente"
            ),
        )
        .join(
            Usuario,
            (Usuario.id == Profissional.usuario_id)
            & (Usuario.empresa_id == Profissional.empresa_id),
        )
        .outerjoin(
            producao, producao.c.profissional_id == Profissional.id
        )
        .outerjoin(
            repassado, repassado.c.profissional_id == Profissional.id
        )
        .outerjoin(pendente, pendente.c.profissional_id == Profissional.id)
        .filter(Profissional.empresa_id == empresa_id)
    )
    if profissional_id is not None:
        query = query.filter(Profissional.id == profissional_id)
    return query.order_by(
        func.coalesce(producao.c.faturamento_bruto, 0).desc(),
        Usuario.nome.asc(),
        Profissional.id.asc(),
    ).all()


def listar_desempenho_servicos(
    db: Session, empresa_id: int, inicio: datetime, fim_exclusivo: datetime
):
    return (
        db.query(
            Servico.id.label("servico_id"),
            Servico.nome,
            func.count(Atendimento.id).label("total_atendimentos"),
            func.sum(Atendimento.valor).label("faturamento_bruto"),
        )
        .join(
            Atendimento,
            (Atendimento.servico_id == Servico.id)
            & (Atendimento.empresa_id == Servico.empresa_id),
        )
        .filter(
            Servico.empresa_id == empresa_id,
            *_filtro_periodo(Atendimento.realizado_em, inicio, fim_exclusivo),
        )
        .group_by(Servico.id, Servico.nome)
        .order_by(func.sum(Atendimento.valor).desc(), Servico.nome.asc())
        .all()
    )


def listar_desempenho_formas_pagamento(
    db: Session, empresa_id: int, inicio: datetime, fim_exclusivo: datetime
):
    return (
        db.query(
            Atendimento.forma_pagamento,
            func.count(Atendimento.id).label("total_atendimentos"),
            func.sum(Atendimento.valor).label("faturamento_bruto"),
        )
        .filter(
            Atendimento.empresa_id == empresa_id,
            *_filtro_periodo(Atendimento.realizado_em, inicio, fim_exclusivo),
        )
        .group_by(Atendimento.forma_pagamento)
        .order_by(func.sum(Atendimento.valor).desc(), Atendimento.forma_pagamento)
        .all()
    )
