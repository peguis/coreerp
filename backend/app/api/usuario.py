from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.services.usuario import (
    criar_usuario_service,
    listar_usuarios_service
)
from fastapi import HTTPException

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.post(
    "/",
    response_model=UsuarioResponse
)
def criar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    return criar_usuario_service(
        db,
        usuario
    )

@router.get("/")
def listar_usuarios_endpoint(
    db: Session = Depends(get_db)
):
    return listar_usuarios_service(db)

@router.get("/{usuario_id}")
def buscar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    usuario = buscar_usuario_service(db, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario

@router.put("/{usuario_id}")
def editar_usuario(
    usuario_id: int,
    dados: dict,
    db: Session = Depends(get_db)
):
    usuario = atualizar_usuario_service(
        db,
        usuario_id,
        dados
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario

@router.delete("/{usuario_id}")
def remover_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    sucesso = deletar_usuario_service(
        db,
        usuario_id
    )

    if not sucesso:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return {
        "mensagem": "Usuário removido"
    }