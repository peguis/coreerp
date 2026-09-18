from calendar import monthrange
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.dashboard_piloto import (
    listar_atendimentos_para_grafico,
    listar_desempenho_formas_pagamento,
    listar_desempenho_profissionais,
    listar_desempenho_servicos,
    listar_ultimos_atendimentos,
    obter_caixa_piloto,
    obter_total_pendente,
    obter_total_repassado,
    obter_totais_producao,
)
from app.repositories.profissional import buscar_profissional_por_usuario


def _decimal(value) -> Decimal:
    return Decimal(str(value or 0)).quantize(Decimal("0.01"))


def _resolver_periodo(data_inicio: date | None, data_fim: date | None):
    hoje = date.today()
    inicio_padrao = hoje.replace(day=1)
    fim_padrao = hoje.replace(day=monthrange(hoje.year, hoje.month)[1])
    inicio_data = data_inicio or inicio_padrao
    fim_data = data_fim or fim_padrao
    if inicio_data > fim_data:
        raise HTTPException(
            status_code=400,
            detail="data_inicio deve ser menor ou igual a data_fim.",
        )
    inicio = datetime.combine(inicio_data, time.min, tzinfo=timezone.utc)
    fim_exclusivo = datetime.combine(
        fim_data + timedelta(days=1), time.min, tzinfo=timezone.utc
    )
    return inicio_data, fim_data, inicio, fim_exclusivo


def _mapear_profissional(row):
    return {
        "profissional_id": row.profissional_id,
        "nome": row.nome,
        "area_atuacao": row.area_atuacao,
        "quantidade_atendimentos": int(row.total_atendimentos or 0),
        "faturamento_bruto": _decimal(row.faturamento_bruto),
        "valor_profissional": _decimal(row.valor_profissional),
        "valor_casa": _decimal(row.valor_casa),
        "valor_repassado": _decimal(row.total_repassado),
        "valor_pendente": _decimal(row.total_pendente),
    }


def buscar_dashboard_piloto_service(
    db: Session, usuario, data_inicio: date | None, data_fim: date | None
):
    inicio_data, fim_data, inicio, fim_exclusivo = _resolver_periodo(
        data_inicio, data_fim
    )
    empresa_id = usuario.empresa_id
    producao = obter_totais_producao(db, empresa_id, inicio, fim_exclusivo)
    total_repassado = _decimal(
        obter_total_repassado(db, empresa_id, inicio, fim_exclusivo)
    )
    total_pendente = _decimal(
        obter_total_pendente(db, empresa_id, inicio, fim_exclusivo)
    )
    # O Financeiro legado usa timestamp sem timezone; P3/P5 usam UTC com timezone.
    caixa = obter_caixa_piloto(
        db,
        empresa_id,
        inicio.replace(tzinfo=None),
        fim_exclusivo.replace(tzinfo=None),
    )
    entradas = _decimal(caixa.entradas)
    saidas = _decimal(caixa.saidas)

    profissionais = [
        _mapear_profissional(row)
        for row in listar_desempenho_profissionais(
            db, empresa_id, inicio, fim_exclusivo
        )
    ]
    servicos = [
        {
            "servico_id": row.servico_id,
            "nome": row.nome,
            "quantidade": int(row.total_atendimentos),
            "faturamento_bruto": _decimal(row.faturamento_bruto),
        }
        for row in listar_desempenho_servicos(
            db, empresa_id, inicio, fim_exclusivo
        )
    ]
    formas = [
        {
            "forma_pagamento": row.forma_pagamento,
            "quantidade_atendimentos": int(row.total_atendimentos),
            "valor_total": _decimal(row.faturamento_bruto),
        }
        for row in listar_desempenho_formas_pagamento(
            db, empresa_id, inicio, fim_exclusivo
        )
    ]
    faturamento_por_dia_semana = [
        {
            "dia_semana": dia_semana,
            "quantidade_atendimentos": 0,
            "faturamento_bruto": Decimal("0.00"),
        }
        for dia_semana in range(7)
    ]
    for row in listar_atendimentos_para_grafico(
        db, empresa_id, inicio, fim_exclusivo
    ):
        dia_semana = row.realizado_em.weekday()
        faturamento_por_dia_semana[dia_semana]["quantidade_atendimentos"] += 1
        faturamento_por_dia_semana[dia_semana]["faturamento_bruto"] += _decimal(
            row.valor
        )

    ultimos_atendimentos = [
        {
            "atendimento_id": row.atendimento_id,
            "cliente_nome": row.cliente_nome,
            "servico_nome": row.servico_nome,
            "profissional_nome": row.profissional_nome,
            "realizado_em": row.realizado_em,
            "status": "CONCLUIDO",
        }
        for row in listar_ultimos_atendimentos(
            db, empresa_id, inicio, fim_exclusivo
        )
    ]
    return {
        "data_inicio": inicio_data,
        "data_fim": fim_data,
        "total_atendimentos": int(producao.total_atendimentos or 0),
        "faturamento_bruto": _decimal(producao.faturamento_bruto),
        "valor_casa": _decimal(producao.valor_casa),
        "valor_profissionais": _decimal(producao.valor_profissionais),
        "total_repassado": total_repassado,
        "total_pendente_repasses": total_pendente,
        "entradas_caixa_piloto": entradas,
        "saidas_caixa_piloto": saidas,
        "saldo_caixa_piloto": entradas - saidas,
        "por_profissional": profissionais,
        "por_servico": servicos,
        "por_forma_pagamento": formas,
        "faturamento_por_dia_semana": faturamento_por_dia_semana,
        "ultimos_atendimentos": ultimos_atendimentos,
    }


def buscar_dashboard_profissional_service(
    db: Session, usuario, data_inicio: date | None, data_fim: date | None
):
    profissional = buscar_profissional_por_usuario(
        db, usuario.id, usuario.empresa_id
    )
    if not profissional:
        raise HTTPException(
            status_code=403,
            detail="Usuario sem profissional vinculado nesta empresa.",
        )
    inicio_data, fim_data, inicio, fim_exclusivo = _resolver_periodo(
        data_inicio, data_fim
    )
    rows = listar_desempenho_profissionais(
        db,
        usuario.empresa_id,
        inicio,
        fim_exclusivo,
        profissional.id,
    )
    if not rows:
        raise HTTPException(status_code=403, detail="Vinculo profissional invalido.")
    dados = _mapear_profissional(rows[0])
    dados.pop("valor_casa")
    return {"data_inicio": inicio_data, "data_fim": fim_data, **dados}
