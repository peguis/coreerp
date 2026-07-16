from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate, EmpresaResponse
from app.services.empresa import (
    criar_empresa_service,
    listar_empresas_service,
    buscar_empresa_por_id_service,
    atualizar_empresa_service,
    deletar_empresa_service,
)
from fastapi import HTTPException


router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)


@router.post(
    "/",
    response_model=EmpresaResponse
)
def criar_empresa_api(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db)
):
    return criar_empresa(
        db,
        empresa
    )


@router.get(
    "/",
    response_model=list[EmpresaResponse]
)
def listar_empresas(
    db: Session = Depends(get_db)
):
    return db.query(Empresa).all()

@router.get("/")
def listar_empresas_endpoint(
    db: Session = Depends(get_db)
):
    return listar_empresas_service(db)

from app.services.empresa import (
    criar_empresa_service,
    listar_empresas_service,
    buscar_empresa_por_id_service
)

@router.get("/{empresa_id}")
def buscar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    empresa = buscar_empresa_por_id_service(db, empresa_id)

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    return empresa

@router.put("/{empresa_id}")
def atualizar_empresa(
    empresa_id: int,
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
):
    empresa_db = buscar_empresa_por_id_service(db, empresa_id)

    if not empresa_db:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    return atualizar_empresa_service(
        db,
        empresa_db,
        empresa
    )

@router.delete("/{empresa_id}")
def deletar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
):
    empresa_db = buscar_empresa_por_id_service(db, empresa_id)

    if not empresa_db:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    deletar_empresa_service(
        db,
        empresa_db
    )

    return {
        "mensagem": "Empresa removida com sucesso"
    }

