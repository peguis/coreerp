from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import FormaPagamentoRepasse, PerfilUsuario
from app.repositories.profissional import (
    buscar_profissional_por_id,
    buscar_profissional_por_usuario,
)
from app.repositories.repasse import (
    bloquear_atendimentos,
    buscar_repasse_por_id,
    criar_repasse,
    criar_repasse_item,
    listar_atendimentos_pendencia,
    listar_repasses,
    listar_totais_pendencias,
    somar_repassado_por_atendimento,
)
from app.services.integracao_financeira import registrar_saida_repasse


CENTAVOS = Decimal("0.01")
PERFIS_LEITURA = {
    PerfilUsuario.ADMIN.value,
    PerfilUsuario.GERENTE.value,
    PerfilUsuario.PROFISSIONAL.value,
}
PERFIS_CRIACAO = {
    PerfilUsuario.ADMIN.value,
    PerfilUsuario.GERENTE.value,
}


def _decimal_centavos(valor, campo: str) -> Decimal:
    try:
        resultado = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError):
        resultado = None
    if resultado is None or not resultado.is_finite() or resultado <= 0:
        raise HTTPException(
            status_code=400,
            detail=f"{campo} deve ser maior que zero.",
        )
    return resultado.quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def _decimal_nao_negativo(valor) -> Decimal:
    resultado = Decimal(str(valor)).quantize(CENTAVOS, rounding=ROUND_HALF_UP)
    if resultado < 0:
        raise HTTPException(
            status_code=409,
            detail="Saldo de repasse inconsistente.",
        )
    return resultado


def _profissional_do_usuario(db: Session, usuario):
    profissional = buscar_profissional_por_usuario(
        db, usuario.id, usuario.empresa_id
    )
    if not profissional:
        raise HTTPException(
            status_code=403,
            detail="Usuario sem profissional vinculado.",
        )
    return profissional


def criar_repasse_service(db: Session, dados, usuario):
    if usuario.perfil not in PERFIS_CRIACAO:
        raise HTTPException(
            status_code=403,
            detail="Sem permissao para criar repasse.",
        )
    profissional = buscar_profissional_por_id(
        db, dados.profissional_id, usuario.empresa_id
    )
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional nao encontrado.")

    ids = [item.atendimento_id for item in dados.itens]
    if len(ids) != len(set(ids)):
        raise HTTPException(
            status_code=400,
            detail="Um atendimento nao pode se repetir no mesmo repasse.",
        )

    try:
        atendimentos = bloquear_atendimentos(db, ids, usuario.empresa_id)
        atendimentos_por_id = {item.id: item for item in atendimentos}
        if len(atendimentos_por_id) != len(ids):
            raise HTTPException(
                status_code=404,
                detail="Atendimento nao encontrado.",
            )

        itens_validados = []
        total = Decimal("0.00")
        for item in dados.itens:
            atendimento = atendimentos_por_id[item.atendimento_id]
            if atendimento.profissional_id != profissional.id:
                raise HTTPException(
                    status_code=400,
                    detail="Atendimento nao pertence ao profissional do repasse.",
                )

            valor_item = _decimal_centavos(item.valor, "Valor do item")
            ja_repassado = _decimal_nao_negativo(
                somar_repassado_por_atendimento(
                    db, atendimento.id, usuario.empresa_id
                )
            )
            devido = _decimal_nao_negativo(atendimento.valor_profissional)
            saldo = devido - ja_repassado
            if saldo < 0 or valor_item > saldo:
                raise HTTPException(
                    status_code=409,
                    detail="Valor do item excede o saldo do atendimento.",
                )
            itens_validados.append((atendimento.id, valor_item))
            total += valor_item

        try:
            forma_pagamento = FormaPagamentoRepasse(
                dados.forma_pagamento
            ).value
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=400,
                detail="Forma de pagamento do repasse invalida.",
            )

        total = total.quantize(CENTAVOS, rounding=ROUND_HALF_UP)
        repasse = criar_repasse(
            db,
            empresa_id=usuario.empresa_id,
            profissional_id=profissional.id,
            created_by_usuario_id=usuario.id,
            valor=total,
            forma_pagamento=forma_pagamento,
            observacao=dados.observacao,
            pago_em=dados.pago_em or datetime.now(timezone.utc),
        )
        for atendimento_id, valor_item in itens_validados:
            criar_repasse_item(
                db,
                empresa_id=usuario.empresa_id,
                repasse_id=repasse.id,
                atendimento_id=atendimento_id,
                valor=valor_item,
            )
        registrar_saida_repasse(db, repasse, usuario)
        db.commit()
        return buscar_repasse_por_id(db, repasse.id, usuario.empresa_id)
    except Exception:
        db.rollback()
        raise


def _resolver_filtro_profissional(
    db: Session,
    usuario,
    profissional_id: int | None,
) -> int | None:
    if usuario.perfil not in PERFIS_LEITURA:
        raise HTTPException(status_code=403, detail="Sem permissao para repasses.")
    if usuario.perfil == PerfilUsuario.PROFISSIONAL.value:
        profissional = _profissional_do_usuario(db, usuario)
        if profissional_id is not None and profissional_id != profissional.id:
            raise HTTPException(
                status_code=403,
                detail="Profissional nao pode consultar repasses de outro.",
            )
        return profissional.id
    if profissional_id is not None:
        profissional = buscar_profissional_por_id(
            db, profissional_id, usuario.empresa_id
        )
        if not profissional:
            raise HTTPException(
                status_code=404,
                detail="Profissional nao encontrado.",
            )
    return profissional_id


def listar_repasses_service(
    db: Session,
    usuario,
    profissional_id: int | None = None,
    pago_de: datetime | None = None,
    pago_ate: datetime | None = None,
    pagina: int = 1,
    limite: int = 10,
):
    profissional_id = _resolver_filtro_profissional(
        db, usuario, profissional_id
    )
    return listar_repasses(
        db,
        usuario.empresa_id,
        profissional_id,
        pago_de,
        pago_ate,
        pagina,
        limite,
    )


def buscar_repasse_service(db: Session, repasse_id: int, usuario):
    if usuario.perfil not in PERFIS_LEITURA:
        raise HTTPException(status_code=403, detail="Sem permissao para repasses.")
    repasse = buscar_repasse_por_id(db, repasse_id, usuario.empresa_id)
    if not repasse:
        return None
    if usuario.perfil == PerfilUsuario.PROFISSIONAL.value:
        profissional = _profissional_do_usuario(db, usuario)
        if repasse.profissional_id != profissional.id:
            return None
    return repasse


def listar_pendencias_service(
    db: Session,
    usuario,
    profissional_id: int | None = None,
):
    profissional_id = _resolver_filtro_profissional(
        db, usuario, profissional_id
    )
    totais = listar_totais_pendencias(
        db, usuario.empresa_id, profissional_id
    )
    detalhar = profissional_id is not None
    resultado = []
    for total in totais:
        devido = _decimal_nao_negativo(total.total_devido)
        repassado = _decimal_nao_negativo(total.total_repassado)
        pendente = devido - repassado
        if pendente < 0:
            raise HTTPException(
                status_code=409,
                detail="Saldo de repasse inconsistente.",
            )
        atendimentos = []
        if detalhar:
            for item in listar_atendimentos_pendencia(
                db, usuario.empresa_id, total.profissional_id
            ):
                valor_profissional = _decimal_nao_negativo(
                    item.valor_profissional
                )
                valor_repassado = _decimal_nao_negativo(
                    item.valor_repassado
                )
                valor_pendente = valor_profissional - valor_repassado
                if valor_pendente < 0:
                    raise HTTPException(
                        status_code=409,
                        detail="Saldo de atendimento inconsistente.",
                    )
                atendimentos.append(
                    {
                        "atendimento_id": item.atendimento_id,
                        "realizado_em": item.realizado_em,
                        "valor": Decimal(str(item.valor)),
                        "valor_profissional": valor_profissional,
                        "valor_repassado": valor_repassado,
                        "valor_pendente": valor_pendente,
                    }
                )
        resultado.append(
            {
                "profissional_id": total.profissional_id,
                "total_devido": devido,
                "total_repassado": repassado,
                "total_pendente": pendente,
                "atendimentos": atendimentos,
            }
        )
    return resultado
