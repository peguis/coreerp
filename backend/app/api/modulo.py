from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_perfil
from app.database import get_db
from app.schemas.modulo import ModuloResponse, ModuloStatusUpdate
from app.services.modulo import atualizar_modulo_empresa, listar_modulos_empresa


router = APIRouter(prefix="/modulos", tags=["Módulos"])


@router.get("/", response_model=list[ModuloResponse])
def listar_modulos(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    return listar_modulos_empresa(db, usuario.empresa_id)


@router.patch("/{codigo}", response_model=ModuloResponse)
def atualizar_modulo(
    codigo: str,
    dados: ModuloStatusUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin")),
):
    return atualizar_modulo_empresa(
        db,
        usuario.empresa_id,
        codigo,
        dados.ativo,
    )
