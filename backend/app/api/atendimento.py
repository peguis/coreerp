from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import require_perfil
from app.core.enums import FormaPagamento
from app.database import get_db
from app.schemas.atendimento import AtendimentoCreate, AtendimentoResponse
from app.services.atendimento import (
    buscar_atendimento_service,
    criar_atendimento_service,
    listar_atendimentos_service,
)


router = APIRouter(prefix="/atendimentos", tags=["Atendimentos"])
perfis_atendimento = require_perfil("admin", "gerente", "profissional")


@router.post("/", response_model=AtendimentoResponse)
def criar_atendimento_endpoint(
    dados: AtendimentoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(perfis_atendimento),
):
    return criar_atendimento_service(db, dados, usuario)


@router.get("/", response_model=list[AtendimentoResponse])
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
    return listar_atendimentos_service(
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


@router.get("/{atendimento_id}", response_model=AtendimentoResponse)
def buscar_atendimento_endpoint(
    atendimento_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(perfis_atendimento),
):
    atendimento = buscar_atendimento_service(db, atendimento_id, usuario)
    if not atendimento:
        raise HTTPException(status_code=404, detail="Atendimento nao encontrado.")
    return atendimento
