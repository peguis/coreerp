from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import require_perfil
from app.database import get_db
from app.schemas.repasse import (
    PendenciaProfissionalResponse,
    RepasseCreate,
    RepasseResponse,
)
from app.services.repasse import (
    buscar_repasse_service,
    criar_repasse_service,
    listar_pendencias_service,
    listar_repasses_service,
)


router = APIRouter(prefix="/repasses", tags=["Repasses"])
perfis_leitura = require_perfil("admin", "gerente", "profissional")


@router.post("/", response_model=RepasseResponse)
def criar_repasse_endpoint(
    dados: RepasseCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente")),
):
    return criar_repasse_service(db, dados, usuario)


@router.get("/", response_model=list[RepasseResponse])
def listar_repasses_endpoint(
    profissional_id: int | None = Query(None, gt=0),
    pago_de: datetime | None = Query(None),
    pago_ate: datetime | None = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    usuario=Depends(perfis_leitura),
):
    return listar_repasses_service(
        db,
        usuario,
        profissional_id,
        pago_de,
        pago_ate,
        pagina,
        limite,
    )


@router.get(
    "/pendencias",
    response_model=list[PendenciaProfissionalResponse],
)
def listar_pendencias_endpoint(
    profissional_id: int | None = Query(None, gt=0),
    db: Session = Depends(get_db),
    usuario=Depends(perfis_leitura),
):
    return listar_pendencias_service(db, usuario, profissional_id)


@router.get("/{repasse_id}", response_model=RepasseResponse)
def buscar_repasse_endpoint(
    repasse_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(perfis_leitura),
):
    repasse = buscar_repasse_service(db, repasse_id, usuario)
    if not repasse:
        raise HTTPException(status_code=404, detail="Repasse nao encontrado.")
    return repasse
