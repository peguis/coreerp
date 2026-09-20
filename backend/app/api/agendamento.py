from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_modulo, require_perfil
from app.core.enums import StatusAgendamento
from app.database import get_db
from app.schemas.agendamento import (
    AgendamentoCreate,
    AgendamentoResponse,
    AgendamentoUpdate,
)
from app.services.agendamento import (
    atualizar_agendamento_service,
    buscar_agendamento_service,
    criar_agendamento_service,
    listar_agendamentos_service,
)


router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"],
    dependencies=[Depends(require_modulo("agenda"))],
)
perfis_agenda = require_perfil("admin", "gerente", "profissional")


@router.post(
    "/",
    response_model=AgendamentoResponse,
)
def criar_agendamento_endpoint(
    dados: AgendamentoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(perfis_agenda),
):
    agendamento = criar_agendamento_service(db, dados, usuario)
    return buscar_agendamento_service(db, agendamento.id, usuario)


@router.get(
    "/",
    response_model=list[AgendamentoResponse],
)
def listar_agendamentos_endpoint(
    inicio_de: datetime | None = Query(None),
    inicio_ate: datetime | None = Query(None),
    profissional_id: int | None = Query(None, gt=0),
    recurso_id: int | None = Query(None, gt=0),
    status: StatusAgendamento | None = Query(None),
    db: Session = Depends(get_db),
    usuario=Depends(perfis_agenda),
):
    return listar_agendamentos_service(
        db,
        usuario,
        inicio_de=inicio_de,
        inicio_ate=inicio_ate,
        profissional_id=profissional_id,
        recurso_id=recurso_id,
        status=status.value if status else None,
    )


@router.get(
    "/{agendamento_id}",
    response_model=AgendamentoResponse,
)
def buscar_agendamento_endpoint(
    agendamento_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(perfis_agenda),
):
    agendamento = buscar_agendamento_service(db, agendamento_id, usuario)
    if not agendamento:
        raise HTTPException(
            status_code=404,
            detail="Agendamento nao encontrado.",
        )
    return agendamento


@router.patch(
    "/{agendamento_id}",
    response_model=AgendamentoResponse,
)
def atualizar_agendamento_endpoint(
    agendamento_id: int,
    dados: AgendamentoUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(perfis_agenda),
):
    agendamento = atualizar_agendamento_service(
        db, agendamento_id, dados, usuario
    )
    return buscar_agendamento_service(db, agendamento.id, usuario)
