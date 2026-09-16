from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import OrigemLancamento
from app.repositories.integracao_financeira import (
    criar_lancamento_automatico,
    obter_ou_criar_categoria_sistema,
)


CENTAVOS = Decimal("0.01")


def _valor_monetario(valor) -> Decimal:
    try:
        resultado = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError):
        resultado = None
    if resultado is None or not resultado.is_finite() or resultado <= 0:
        raise HTTPException(
            status_code=400,
            detail="Valor financeiro automatico invalido.",
        )
    return resultado.quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def registrar_entrada_atendimento(db: Session, atendimento, usuario):
    if (
        atendimento.empresa_id is None
        or atendimento.id is None
        or atendimento.empresa_id != usuario.empresa_id
    ):
        raise HTTPException(
            status_code=400,
            detail="Atendimento sem identidade financeira valida.",
        )
    categoria = obter_ou_criar_categoria_sistema(
        db,
        empresa_id=atendimento.empresa_id,
        chave="RECEITA_SERVICOS",
        nome="Receita de Servicos",
        tipo="RECEITA",
    )
    db.flush()
    return criar_lancamento_automatico(
        db,
        empresa_id=atendimento.empresa_id,
        usuario_id=usuario.id,
        categoria_id=categoria.id,
        descricao=f"Atendimento #{atendimento.id}",
        valor=_valor_monetario(atendimento.valor),
        tipo="RECEITA",
        status="RECEBIDO",
        data_movimento=atendimento.realizado_em,
        forma_pagamento=atendimento.forma_pagamento,
        origem_tipo=OrigemLancamento.ATENDIMENTO.value,
        origem_id=atendimento.id,
    )


def registrar_saida_repasse(db: Session, repasse, usuario):
    if (
        repasse.empresa_id is None
        or repasse.id is None
        or repasse.empresa_id != usuario.empresa_id
    ):
        raise HTTPException(
            status_code=400,
            detail="Repasse sem identidade financeira valida.",
        )
    categoria = obter_ou_criar_categoria_sistema(
        db,
        empresa_id=repasse.empresa_id,
        chave="REPASSE_PROFISSIONAIS",
        nome="Repasse a Profissionais",
        tipo="DESPESA",
    )
    db.flush()
    return criar_lancamento_automatico(
        db,
        empresa_id=repasse.empresa_id,
        usuario_id=usuario.id,
        categoria_id=categoria.id,
        descricao=f"Repasse profissional #{repasse.id}",
        valor=_valor_monetario(repasse.valor),
        tipo="DESPESA",
        status="PAGO",
        data_movimento=repasse.pago_em,
        forma_pagamento=repasse.forma_pagamento,
        origem_tipo=OrigemLancamento.REPASSE.value,
        origem_id=repasse.id,
    )
