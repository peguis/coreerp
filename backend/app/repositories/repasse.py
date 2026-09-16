from datetime import datetime
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from app.models.atendimento import Atendimento
from app.models.profissional import Profissional
from app.models.repasse import Repasse, RepasseItem


def bloquear_atendimentos(
    db: Session,
    atendimento_ids: list[int],
    empresa_id: int,
) -> list[Atendimento]:
    return (
        db.query(Atendimento)
        .filter(
            Atendimento.id.in_(sorted(atendimento_ids)),
            Atendimento.empresa_id == empresa_id,
        )
        .order_by(Atendimento.id.asc())
        .with_for_update()
        .all()
    )


def somar_repassado_por_atendimento(
    db: Session,
    atendimento_id: int,
    empresa_id: int,
) -> Decimal:
    return (
        db.query(func.coalesce(func.sum(RepasseItem.valor), 0))
        .filter(
            RepasseItem.atendimento_id == atendimento_id,
            RepasseItem.empresa_id == empresa_id,
        )
        .scalar()
    )


def criar_repasse(
    db: Session,
    *,
    empresa_id: int,
    profissional_id: int,
    created_by_usuario_id: int,
    valor: Decimal,
    forma_pagamento: str,
    observacao: str | None,
    pago_em: datetime,
) -> Repasse:
    repasse = Repasse(
        empresa_id=empresa_id,
        profissional_id=profissional_id,
        created_by_usuario_id=created_by_usuario_id,
        valor=valor,
        forma_pagamento=forma_pagamento,
        observacao=observacao,
        pago_em=pago_em,
    )
    db.add(repasse)
    db.flush()
    return repasse


def criar_repasse_item(
    db: Session,
    *,
    empresa_id: int,
    repasse_id: int,
    atendimento_id: int,
    valor: Decimal,
) -> RepasseItem:
    item = RepasseItem(
        empresa_id=empresa_id,
        repasse_id=repasse_id,
        atendimento_id=atendimento_id,
        valor=valor,
    )
    db.add(item)
    db.flush()
    return item


def buscar_repasse_por_id(
    db: Session,
    repasse_id: int,
    empresa_id: int,
) -> Repasse | None:
    return (
        db.query(Repasse)
        .options(selectinload(Repasse.itens))
        .filter(
            Repasse.id == repasse_id,
            Repasse.empresa_id == empresa_id,
        )
        .first()
    )


def listar_repasses(
    db: Session,
    empresa_id: int,
    profissional_id: int | None = None,
    pago_de: datetime | None = None,
    pago_ate: datetime | None = None,
    pagina: int = 1,
    limite: int = 10,
) -> list[Repasse]:
    query = (
        db.query(Repasse)
        .options(selectinload(Repasse.itens))
        .filter(Repasse.empresa_id == empresa_id)
    )
    if profissional_id is not None:
        query = query.filter(Repasse.profissional_id == profissional_id)
    if pago_de is not None:
        query = query.filter(Repasse.pago_em >= pago_de)
    if pago_ate is not None:
        query = query.filter(Repasse.pago_em <= pago_ate)
    return (
        query.order_by(Repasse.pago_em.desc(), Repasse.id.desc())
        .offset((pagina - 1) * limite)
        .limit(limite)
        .all()
    )


def listar_totais_pendencias(
    db: Session,
    empresa_id: int,
    profissional_id: int | None = None,
):
    devidos = (
        db.query(
            Atendimento.profissional_id.label("profissional_id"),
            func.sum(Atendimento.valor_profissional).label("total_devido"),
        )
        .filter(Atendimento.empresa_id == empresa_id)
        .group_by(Atendimento.profissional_id)
        .subquery()
    )
    repassados = (
        db.query(
            Atendimento.profissional_id.label("profissional_id"),
            func.sum(RepasseItem.valor).label("total_repassado"),
        )
        .join(
            RepasseItem,
            (RepasseItem.atendimento_id == Atendimento.id)
            & (RepasseItem.empresa_id == Atendimento.empresa_id),
        )
        .filter(Atendimento.empresa_id == empresa_id)
        .group_by(Atendimento.profissional_id)
        .subquery()
    )
    query = (
        db.query(
            Profissional.id.label("profissional_id"),
            func.coalesce(devidos.c.total_devido, 0).label("total_devido"),
            func.coalesce(repassados.c.total_repassado, 0).label(
                "total_repassado"
            ),
        )
        .outerjoin(devidos, devidos.c.profissional_id == Profissional.id)
        .outerjoin(
            repassados, repassados.c.profissional_id == Profissional.id
        )
        .filter(Profissional.empresa_id == empresa_id)
    )
    if profissional_id is not None:
        query = query.filter(Profissional.id == profissional_id)
    return query.order_by(Profissional.id.asc()).all()


def listar_atendimentos_pendencia(
    db: Session,
    empresa_id: int,
    profissional_id: int,
):
    repassados = (
        db.query(
            RepasseItem.atendimento_id.label("atendimento_id"),
            func.sum(RepasseItem.valor).label("valor_repassado"),
        )
        .filter(RepasseItem.empresa_id == empresa_id)
        .group_by(RepasseItem.atendimento_id)
        .subquery()
    )
    return (
        db.query(
            Atendimento.id.label("atendimento_id"),
            Atendimento.realizado_em,
            Atendimento.valor,
            Atendimento.valor_profissional,
            func.coalesce(repassados.c.valor_repassado, 0).label(
                "valor_repassado"
            ),
        )
        .outerjoin(
            repassados, repassados.c.atendimento_id == Atendimento.id
        )
        .filter(
            Atendimento.empresa_id == empresa_id,
            Atendimento.profissional_id == profissional_id,
        )
        .order_by(Atendimento.realizado_em.asc(), Atendimento.id.asc())
        .all()
    )
