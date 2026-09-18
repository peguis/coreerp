from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_perfil
from app.database import get_db
from app.schemas.recurso_agenda import (
    RecursoAgendaCreate,
    RecursoAgendaResponse,
    RecursoAgendaUpdate,
)
from app.services.recurso_agenda import (
    atualizar_recurso_service,
    criar_recurso_service,
    listar_recursos_service,
)


router = APIRouter(prefix="/recursos-agenda", tags=["Recursos da Agenda"])


@router.post(
    "/",
    response_model=RecursoAgendaResponse,
)
def criar_recurso_endpoint(
    dados: RecursoAgendaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente")),
):
    return criar_recurso_service(db, dados, usuario.empresa_id)


@router.get(
    "/",
    response_model=list[RecursoAgendaResponse],
)
def listar_recursos_endpoint(
    tipo: str | None = Query(None),
    ativo: bool | None = Query(None),
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_recursos_service(db, usuario.empresa_id, tipo, ativo)


@router.put(
    "/{recurso_id}",
    response_model=RecursoAgendaResponse,
)
def atualizar_recurso_endpoint(
    recurso_id: int,
    dados: RecursoAgendaUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente")),
):
    return atualizar_recurso_service(
        db, recurso_id, dados, usuario.empresa_id
    )
