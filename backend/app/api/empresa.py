from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate, EmpresaResponse
from app.services.empresa import criar_empresa


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