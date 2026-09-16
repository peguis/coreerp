from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import require_perfil
from app.core.enums import FormaPagamento
from app.database import get_db
from app.schemas.atendimento import (
    AtendimentoCreate,
    AtendimentoProfissionalResponse,
    AtendimentoResponse,
)
from app.services.atendimento import (
    buscar_atendimento_service,
    criar_atendimento_service,
    listar_atendimentos_service,
)


router = APIRouter(prefix="/atendimentos", tags=["Atendimentos"])
perfis_atendimento = require_perfil("admin", "gerente", "profissional")
RespostaAtendimento = AtendimentoResponse | AtendimentoProfissionalResponse


def _resposta_por_perfil(atendimento, usuario):
    schema = (
        AtendimentoProfissionalResponse
        if usuario.perfil == "profissional"
        else AtendimentoResponse
    )
    return schema.model_validate(atendimento)


@router.post("/", response_model=RespostaAtendimento)
def criar_atendimento_endpoint(
    dados: AtendimentoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(perfis_atendimento),
):
    atendimento = criar_atendimento_service(db, dados, usuario)
    return _resposta_por_perfil(atendimento, usuario)


@router.get("/", response_model=list[RespostaAtendimento])
def listar_atendimentos_endpoint(
    profissional_id: int | None = Query(None, gt=0),
    servico_id: int | None = Query(None, gt=0),
    cliente_id: int | None = Query(None, gt=0),
    forma_pagamento: FormaPagamento | None = Query(None),
    realizado_de: datetime | None = Query(None),
    realizado_ate: datetime | None = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    usuario=Depends(perfis_atendimento),
):
    atendimentos = listar_atendimentos_service(
        db,
        usuario,
        profissional_id,
        servico_id,
        cliente_id,
        forma_pagamento,
        realizado_de,
        realizado_ate,
        pagina,
        limite,
    )
    return [
        _resposta_por_perfil(atendimento, usuario)
        for atendimento in atendimentos
    ]


@router.get("/{atendimento_id}", response_model=RespostaAtendimento)
def buscar_atendimento_endpoint(
    atendimento_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(perfis_atendimento),
):
    atendimento = buscar_atendimento_service(db, atendimento_id, usuario)
    if not atendimento:
        raise HTTPException(status_code=404, detail="Atendimento nao encontrado.")
    return _resposta_por_perfil(atendimento, usuario)
