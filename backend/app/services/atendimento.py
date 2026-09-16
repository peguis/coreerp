from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import FormaPagamento, PerfilUsuario
from app.repositories.atendimento import (
    buscar_atendimento_por_id,
    criar_atendimento,
    listar_atendimentos,
)
from app.repositories.cliente import buscar_cliente_por_id
from app.repositories.profissional import (
    buscar_profissional_por_id,
    buscar_profissional_por_usuario,
)
from app.repositories.servico import buscar_servico_por_id
from app.services.integracao_financeira import registrar_entrada_atendimento


PERFIS_ATENDIMENTO = {
    PerfilUsuario.ADMIN.value,
    PerfilUsuario.GERENTE.value,
    PerfilUsuario.PROFISSIONAL.value,
}
CENTAVOS = Decimal("0.01")
CEM = Decimal("100")


def _validar_perfil(usuario) -> None:
    if usuario.perfil not in PERFIS_ATENDIMENTO:
        raise HTTPException(
            status_code=403,
            detail="Sem permissao para acessar atendimentos.",
        )


def _resolver_profissional_criacao(db: Session, dados, usuario):
    _validar_perfil(usuario)
    if usuario.perfil == PerfilUsuario.PROFISSIONAL.value:
        profissional = buscar_profissional_por_usuario(
            db, usuario.id, usuario.empresa_id
        )
        if not profissional:
            raise HTTPException(
                status_code=403,
                detail="Usuario sem profissional vinculado.",
            )
        if (
            dados.profissional_id is not None
            and dados.profissional_id != profissional.id
        ):
            raise HTTPException(
                status_code=403,
                detail="Profissional nao pode registrar para outro profissional.",
            )
    else:
        if dados.profissional_id is None:
            raise HTTPException(
                status_code=400,
                detail="profissional_id e obrigatorio para admin e gerente.",
            )
        profissional = buscar_profissional_por_id(
            db, dados.profissional_id, usuario.empresa_id
        )
        if not profissional:
            raise HTTPException(
                status_code=404,
                detail="Profissional nao encontrado.",
            )

    if not profissional.ativo:
        raise HTTPException(
            status_code=400,
            detail="Profissional inativo.",
        )
    return profissional


def _normalizar_valor(valor) -> Decimal:
    try:
        valor_decimal = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError):
        valor_decimal = None
    if valor_decimal is None or not valor_decimal.is_finite() or valor_decimal <= 0:
        raise HTTPException(
            status_code=400,
            detail="O valor deve ser maior que zero.",
        )
    return valor_decimal.quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def _calcular_snapshot(valor: Decimal, percentual_origem):
    try:
        percentual = Decimal(str(percentual_origem))
    except (InvalidOperation, TypeError, ValueError):
        percentual = None

    if (
        percentual is None
        or not percentual.is_finite()
        or percentual < 0
        or percentual > CEM
    ):
        raise HTTPException(
            status_code=400,
            detail="Percentual do profissional inconsistente.",
        )

    percentual = percentual.quantize(CENTAVOS, rounding=ROUND_HALF_UP)
    valor_profissional = (
        valor * percentual / CEM
    ).quantize(CENTAVOS, rounding=ROUND_HALF_UP)
    valor_casa = valor - valor_profissional

    if (
        valor_profissional < 0
        or valor_casa < 0
        or valor_profissional > valor
        or valor_casa > valor
        or valor_profissional + valor_casa != valor
    ):
        raise HTTPException(
            status_code=400,
            detail="Divisao financeira inconsistente.",
        )
    return percentual, valor_profissional, valor_casa


def criar_atendimento_service(db: Session, dados, usuario):
    if (
        usuario.perfil == PerfilUsuario.PROFISSIONAL.value
        and dados.percentual_profissional_override is not None
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                "Profissional nao possui permissao para alterar o percentual "
                "de comissao do atendimento."
            ),
        )
    profissional = _resolver_profissional_criacao(db, dados, usuario)

    servico = buscar_servico_por_id(db, dados.servico_id, usuario.empresa_id)
    if not servico:
        raise HTTPException(status_code=404, detail="Servico nao encontrado.")
    if not servico.ativo:
        raise HTTPException(status_code=400, detail="Servico inativo.")

    if dados.cliente_id is not None:
        cliente = buscar_cliente_por_id(
            db, dados.cliente_id, usuario.empresa_id
        )
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente nao encontrado.")

    valor = _normalizar_valor(dados.valor)
    percentual_origem = profissional.percentual_padrao
    if dados.percentual_profissional_override is not None:
        percentual_origem = dados.percentual_profissional_override
    percentual, valor_profissional, valor_casa = _calcular_snapshot(
        valor, percentual_origem
    )
    try:
        forma_pagamento = FormaPagamento(dados.forma_pagamento).value
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Forma de pagamento invalida.",
        )

    try:
        atendimento = criar_atendimento(
            db,
            empresa_id=usuario.empresa_id,
            profissional_id=profissional.id,
            servico_id=servico.id,
            cliente_id=dados.cliente_id,
            valor=valor,
            percentual_profissional=percentual,
            valor_profissional=valor_profissional,
            valor_casa=valor_casa,
            forma_pagamento=forma_pagamento,
            observacao=dados.observacao,
            realizado_em=dados.realizado_em or datetime.now(timezone.utc),
        )
        registrar_entrada_atendimento(db, atendimento, usuario)
        db.commit()
        db.refresh(atendimento)
        return atendimento
    except Exception:
        db.rollback()
        raise


def _profissional_visivel(db: Session, usuario):
    if usuario.perfil != PerfilUsuario.PROFISSIONAL.value:
        return None
    profissional = buscar_profissional_por_usuario(
        db, usuario.id, usuario.empresa_id
    )
    if not profissional:
        raise HTTPException(
            status_code=403,
            detail="Usuario sem profissional vinculado.",
        )
    return profissional


def listar_atendimentos_service(
    db: Session,
    usuario,
    profissional_id: int | None = None,
    servico_id: int | None = None,
    cliente_id: int | None = None,
    forma_pagamento=None,
    realizado_de: datetime | None = None,
    realizado_ate: datetime | None = None,
    pagina: int = 1,
    limite: int = 10,
):
    _validar_perfil(usuario)
    profissional = _profissional_visivel(db, usuario)
    if profissional:
        if profissional_id is not None and profissional_id != profissional.id:
            raise HTTPException(
                status_code=403,
                detail="Profissional nao pode consultar atendimentos de outro profissional.",
            )
        profissional_id = profissional.id

    forma = (
        FormaPagamento(forma_pagamento).value
        if forma_pagamento is not None
        else None
    )
    return listar_atendimentos(
        db,
        usuario.empresa_id,
        profissional_id,
        servico_id,
        cliente_id,
        forma,
        realizado_de,
        realizado_ate,
        pagina,
        limite,
    )


def buscar_atendimento_service(
    db: Session,
    atendimento_id: int,
    usuario,
):
    _validar_perfil(usuario)
    atendimento = buscar_atendimento_por_id(
        db, atendimento_id, usuario.empresa_id
    )
    if not atendimento:
        return None

    profissional = _profissional_visivel(db, usuario)
    if profissional and atendimento.profissional_id != profissional.id:
        return None
    return atendimento
