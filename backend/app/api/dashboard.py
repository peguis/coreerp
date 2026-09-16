from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user, require_perfil

from app.schemas.dashboard_piloto import (
    DashboardPilotoResponse,
    DashboardProfissionalResponse,
)

from app.services.dashboard import (
    buscar_dashboard_service
)
from app.services.dashboard_piloto import (
    buscar_dashboard_piloto_service,
    buscar_dashboard_profissional_service,
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard(
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user)
):

    return buscar_dashboard_service(
        db,
        usuario
    )


@router.get("/piloto", response_model=DashboardPilotoResponse)
def dashboard_piloto(
    data_inicio: date | None = Query(None),
    data_fim: date | None = Query(None),
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente")),
):
    return buscar_dashboard_piloto_service(
        db, usuario, data_inicio, data_fim
    )


@router.get(
    "/profissional/me", response_model=DashboardProfissionalResponse
)
def dashboard_profissional_me(
    data_inicio: date | None = Query(None),
    data_fim: date | None = Query(None),
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("profissional")),
):
    return buscar_dashboard_profissional_service(
        db, usuario, data_inicio, data_fim
    )
