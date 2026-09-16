from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.atendimento import Atendimento


def criar_atendimento(
    db: Session,
    *,
    empresa_id: int,
    profissional_id: int,
    servico_id: int,
    cliente_id: int | None,
    valor: Decimal,
    percentual_profissional: Decimal,
    valor_profissional: Decimal,
    valor_casa: Decimal,
    forma_pagamento: str,
    observacao: str | None,
    realizado_em: datetime,
) -> Atendimento:
    atendimento = Atendimento(
        empresa_id=empresa_id,
        profissional_id=profissional_id,
        servico_id=servico_id,
        cliente_id=cliente_id,
        valor=valor,
        percentual_profissional=percentual_profissional,
        valor_profissional=valor_profissional,
        valor_casa=valor_casa,
        forma_pagamento=forma_pagamento,
        observacao=observacao,
        realizado_em=realizado_em,
    )
    db.add(atendimento)
    db.flush()
    return atendimento


def buscar_atendimento_por_id(
    db: Session,
    atendimento_id: int,
    empresa_id: int,
) -> Atendimento | None:
    return (
        db.query(Atendimento)
        .filter(
            Atendimento.id == atendimento_id,
            Atendimento.empresa_id == empresa_id,
        )
        .first()
    )


def listar_atendimentos(
    db: Session,
    empresa_id: int,
    profissional_id: int | None = None,
    servico_id: int | None = None,
    cliente_id: int | None = None,
    forma_pagamento: str | None = None,
    realizado_de: datetime | None = None,
    realizado_ate: datetime | None = None,
    pagina: int = 1,
    limite: int = 10,
) -> list[Atendimento]:
    query = db.query(Atendimento).filter(
        Atendimento.empresa_id == empresa_id
    )

    if profissional_id is not None:
        query = query.filter(Atendimento.profissional_id == profissional_id)
    if servico_id is not None:
        query = query.filter(Atendimento.servico_id == servico_id)
    if cliente_id is not None:
        query = query.filter(Atendimento.cliente_id == cliente_id)
    if forma_pagamento is not None:
        query = query.filter(Atendimento.forma_pagamento == forma_pagamento)
    if realizado_de is not None:
        query = query.filter(Atendimento.realizado_em >= realizado_de)
    if realizado_ate is not None:
        query = query.filter(Atendimento.realizado_em <= realizado_ate)

    return (
        query.order_by(
            Atendimento.realizado_em.desc(),
            Atendimento.id.desc(),
        )
        .offset((pagina - 1) * limite)
        .limit(limite)
        .all()
    )
